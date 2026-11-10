"""Modelo de navegação GUIDE: Module -> Section -> Document.

Módulo puro (sem rede, sem Pinecone/OpenAI): constrói uma estrutura
determinística de navegação a partir da hierarquia real de pastas e
arquivos sob `knowledge/`, reutilizando `chunking.py` (mesma convenção
`knowledge/<MODULE>/<TOPIC>/arquivo.md` que o índice RAG já usa).

Não se inventa taxonomia: a ordem e os nomes derivam de:
- o número de módulo (01..NN) declarado no `index.md` de cada módulo;
- o nome da pasta de cada tema (`topic`), humanizado;
- o prefixo numérico de cada arquivo (`FE02-08-variaveis.md` -> ordem 8),
  que já reflete a ordem pedagógica real do curso;
- o primeiro heading `#` de cada arquivo, como título do documento.

Documentos sem `topic` (p.ex. `index.md` ou arquivos soltos direto sob
`<MODULE>/`) não têm uma seção à qual pertencer e ficam fora da
navegação de GUIDE (não se inventa uma categoria "General" para eles).
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from chunking import KNOWLEDGE_DIR, infer_module_topic, iter_markdown_files, read_markdown

_MODULE_NUMBER_RE = re.compile(r"(\d{2})\.\s")
_TITLE_LINE_RE = re.compile(r"^#\s+(.+?)\s*$")
_TITLE_CLEAN_RE = re.compile(r"^\d+\.\s*")
_INDEX_SUFFIX_RE = re.compile(r"\s*[—-]\s*Índice\s*$", re.IGNORECASE)
_DOC_HEADING_RE = re.compile(r"^#\s*[A-Za-z]+\d+(?:-\d+)*\s*[—-]\s*(.+?)\s*$")
_FILENAME_ORDER_RE = re.compile(r"^[A-Za-z]+\d+-(\d+)(?:-(\d+))?-")


@dataclass
class GuideDocument:
    id: str
    title: str
    source: str
    order: float
    topic: str | None = None

    def as_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "source": self.source, "order": self.order, "topic": self.topic}


@dataclass
class GuideSection:
    id: str
    title: str
    order: float
    documents: list[GuideDocument] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "order": self.order,
            "documents": [d.as_dict() for d in self.documents],
        }


@dataclass
class GuideModule:
    id: str
    title: str
    order: float
    sections: list[GuideSection] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "order": self.order,
            "sections": [s.as_dict() for s in self.sections],
        }


def humanize_folder(name: str) -> str:
    """Converte um nome de pasta (`Fundamentos_JS`) em um título legível
    (`Fundamentos JS`), sem alterar a capitalização original de cada
    palavra (já vem em Title Case / siglas desde o nome da pasta)."""
    return name.replace("_", " ").strip()


def _module_order(index_text: str, fallback: float) -> float:
    """Extrai o número do módulo (01..NN) das primeiras linhas do
    `index.md`, seja do título (`# 05. React Avançado`) ou da linha
    descritiva (`... / 01. Fundamentos de HTML e CSS`). Se não encontrar,
    usa `fallback` (ordem alfabética) para não quebrar a construção."""
    for line in index_text.splitlines()[:6]:
        match = _MODULE_NUMBER_RE.search(line)
        if match:
            return float(match.group(1))
    return fallback


def _module_title(index_text: str, fallback: str) -> str:
    for line in index_text.splitlines():
        match = _TITLE_LINE_RE.match(line)
        if match:
            title = _TITLE_CLEAN_RE.sub("", match.group(1))
            title = _INDEX_SUFFIX_RE.sub("", title)
            return title.strip()
    return fallback


def _document_title(text: str, fallback: str) -> str:
    first_line = text.lstrip().split("\n", 1)[0]
    match = _DOC_HEADING_RE.match(first_line) or _TITLE_LINE_RE.match(first_line)
    return match.group(1) if match else fallback


def _document_order(filename: str, fallback: float) -> float:
    match = _FILENAME_ORDER_RE.match(filename)
    if not match:
        return fallback
    main = int(match.group(1))
    sub = int(match.group(2)) if match.group(2) else 0
    return main + sub / 100


def build_guide(root: Path = KNOWLEDGE_DIR) -> list[GuideModule]:
    """Percorre `root` e constrói a hierarquia GUIDE completa, ordenada."""
    modules: dict[str, GuideModule] = {}
    sections: dict[tuple[str, str], GuideSection] = {}

    if not root.is_dir():
        return []
    module_dirs = sorted(p for p in root.iterdir() if p.is_dir() and not p.is_symlink())
    for module_index_order, module_dir in enumerate(module_dirs):
        module_id = module_dir.name.lower()
        index_path = module_dir / "index.md"
        try:
            index_text = read_markdown(index_path) if index_path.exists() else ""
        except (OSError, ValueError):
            index_text = ""
        modules[module_id] = GuideModule(
            id=module_id,
            title=_module_title(index_text, module_dir.name),
            order=_module_order(index_text, float(module_index_order)),
        )

    for path in iter_markdown_files(root):
        module, topic = infer_module_topic(path, root)
        if module is None or topic is None:
            continue  # sem topic não há seção à qual pertencer (não se inventa categoria)

        try:
            text = read_markdown(path)
        except (OSError, ValueError):
            continue
        if not text.strip():
            continue

        module_guide = modules[module]

        section_key = (module, topic)
        topic_dir_name = path.parent.name
        section = sections.get(section_key)
        if section is None:
            section = GuideSection(id=topic, title=humanize_folder(topic_dir_name), order=10_000)
            sections[section_key] = section
            module_guide.sections.append(section)

        doc_order = _document_order(path.name, fallback=10_000)
        section.order = min(section.order, doc_order)
        section.documents.append(
            GuideDocument(
                id=path.stem.lower(),
                title=_document_title(text, fallback=path.stem),
                source=path.relative_to(root).as_posix(),
                order=doc_order,
                topic=topic,
            )
        )

    result = list(modules.values())
    for module_guide in result:
        for section in module_guide.sections:
            section.documents.sort(key=lambda d: d.order)
        module_guide.sections.sort(key=lambda s: s.order)
    result.sort(key=lambda m: m.order)
    return result


def guide_as_list(root: Path = KNOWLEDGE_DIR) -> list[dict]:
    return [m.as_dict() for m in build_guide(root)]


if __name__ == "__main__":
    import json

    print(json.dumps(guide_as_list(), indent=2, ensure_ascii=False))
