"""Chunking de documentos Markdown para o índice RAG.

Módulo puro (sem dependências externas nem efeitos colaterais): divide cada
arquivo em seções `##` respeitando blocos de código, subdividindo apenas as
seções que excederem MAX_CHUNK_CHARS.
"""

import hashlib
import re
from pathlib import Path
from typing import Iterator

KNOWLEDGE_DIR = Path("knowledge")
CHUNK_SIZE = 4000  # tamanho máximo de um chunk, em caracteres
CHUNK_OVERLAP = 200  # sobreposição aplicada apenas ao forçar a subdivisão de seções grandes
MAX_FILE_BYTES = 512 * 1024
RECORD_PREFIX = "dm1-"

MAX_CHUNK_CHARS = CHUNK_SIZE  # alias retro-compatível

_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_SECTION_RE = re.compile(r"^## ")
_SUBSECTION_RE = re.compile(r"^### ")
_BLANK_RE = re.compile(r"^\s*$")
_ANY_LINE_RE = re.compile(r"^.*$")


def _split_on_boundaries(text: str, boundary_re: re.Pattern) -> list[str]:
    """Parte o texto em fragmentos nas linhas que satisfaçam boundary_re,
    ignorando ocorrências dentro de blocos de código fenced. O fence só se
    fecha com uma linha de >= os mesmos backticks com que abriu, assim os
    ``` internos de um bloco ```` não o fecham."""
    fragments, current = [], []
    fence = ""
    for line in text.split("\n"):
        stripped = line.strip()
        if fence:
            current.append(line)
            if stripped.startswith(fence) and set(stripped) == {fence[0]}:
                fence = ""
            continue
        if match := _FENCE_RE.match(line):
            fence = match.group(1)
        elif boundary_re.match(line) and current:
            fragments.append("\n".join(current))
            current = []
        current.append(line)
    fragments.append("\n".join(current))
    return fragments


def split_sections(text: str) -> list[str]:
    """Divide um documento em seções a partir dos seus cabeçalhos `##`.
    A primeira seção inclui o título `#` e qualquer preâmbulo."""
    return [s.strip() for s in _split_on_boundaries(text, _SECTION_RE) if s.strip()]


def extract_heading(section: str) -> str:
    """Devolve o texto do primeiro cabeçalho da seção, ou 'General'."""
    first = section.lstrip().split("\n", 1)[0]
    match = _HEADING_RE.match(first)
    return match.group(1) if match else "General"


def split_large_section(
    section: str, max_chars: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """Subdivide seções que excedam max_chars: primeiro por subseções
    `###`, depois por parágrafos e, como último recurso, por linhas.

    Só nas duas últimas estratégias (forçadas, sem um heading natural que
    as delimite) se aplica `overlap`: repetem-se os últimos `overlap`
    caracteres do chunk anterior no início do seguinte, para não perder
    contexto no corte."""
    if len(section) <= max_chars:
        return [section]

    if max_chars < 1 or overlap < 0:
        raise ValueError("Limites de chunk inválidos.")
    heading_line = section.lstrip().split("\n", 1)[0]
    heading = (
        f"{heading_line}\n\n"
        if _HEADING_RE.match(heading_line) and len(heading_line) + 2 < max_chars // 2
        else ""
    )
    body_limit = max_chars - len(heading)
    overlap = min(overlap, body_limit // 4)
    parts = [section]
    for boundary_re in (_SUBSECTION_RE, _BLANK_RE, _ANY_LINE_RE):
        use_overlap = overlap > 0 and boundary_re is not _SUBSECTION_RE
        pack_limit = body_limit - (overlap + 1 if use_overlap else 0)
        packed = []
        for part in parts:
            if len(part) <= body_limit:
                packed.append(part)
                continue
            local = []
            buf = ""
            for frag in _split_on_boundaries(part, boundary_re):
                if buf and len(buf) + len(frag) + 1 > pack_limit:
                    local.append(buf)
                    buf = frag
                else:
                    buf = f"{buf}\n{frag}" if buf else frag
            if buf:
                local.append(buf)
            if use_overlap:
                for i in range(1, len(local)):
                    tail = local[i - 1][-overlap:]
                    local[i] = f"{tail}\n{local[i]}"
            packed.extend(local)
        parts = packed
        if all(len(p) <= body_limit for p in parts):
            break

    # O limite também vale para uma linha ou fence sem pontos naturais de corte.
    chunks = []
    for part in parts:
        start = 0
        while start < len(part):
            end = min(start + body_limit, len(part))
            chunk = part[start:end].strip()
            if chunk:
                prefix = "" if _HEADING_RE.match(chunk.split("\n", 1)[0]) else heading
                chunks.append(prefix + chunk)
            if end == len(part):
                break
            start = end - overlap
    return chunks


def chunk_markdown(text: str) -> list[dict]:
    """Devolve chunks de um documento: [{'chunk_text': ..., 'section': ...}]."""
    chunks = []
    for section in split_sections(text):
        heading = extract_heading(section)
        for chunk in split_large_section(section):
            chunks.append({"chunk_text": chunk, "section": heading})
    return chunks


def iter_markdown_files(root: Path = KNOWLEDGE_DIR) -> Iterator[Path]:
    yield from sorted(path for path in root.rglob("*") if path.suffix.lower() == ".md")


def read_markdown(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError("arquivo Markdown deve ser regular e não pode ser um link simbólico")
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("arquivo excede 512 KiB")
    if b"\x00" in data:
        raise ValueError("arquivo contém dados binários")
    return data.decode("utf-8-sig")


def infer_module_topic(path: Path, root: Path = KNOWLEDGE_DIR) -> tuple[str | None, str | None]:
    """Infere (module, topic) a partir da localização real do arquivo sob
    `root`, assumindo a convenção `knowledge/<MODULE>/<TOPIC>/arquivo.md`.

    Baseia-se apenas na estrutura de pastas existente, sem inventar
    categorias: se o arquivo está direto sob `root` não há module nem
    topic; se está um nível abaixo (p.ex. `HTML_CSS/index.md`) só há
    module."""
    parts = path.relative_to(root).parts[:-1]  # pastas intermediárias, sem o nome do arquivo
    module = parts[0].lower() if len(parts) >= 1 else None
    topic = parts[1].lower() if len(parts) >= 2 else None
    return module, topic


def build_records(root: Path = KNOWLEDGE_DIR) -> list[dict]:
    return [
        record
        for path in iter_markdown_files(root)
        for record in document_records(path, root, chunk_markdown(read_markdown(path)))
    ]


def document_records(path: Path, root: Path, chunks: list[dict]) -> Iterator[dict]:
    source = path.relative_to(root).as_posix()
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    module, topic = infer_module_topic(path, root)
    scope = {key: value for key, value in (("module", module), ("topic", topic)) if value is not None}
    for i, chunk in enumerate(chunks):
        yield {"_id": f"{record_prefix(module or '')}{digest}-{i}", "source": source, "chunk_id": i, **chunk, **scope}


def record_prefix(module: str | None) -> str:
    if module is None:
        return RECORD_PREFIX
    return f"{RECORD_PREFIX}{hashlib.sha256(module.encode('utf-8')).hexdigest()[:16]}-"
