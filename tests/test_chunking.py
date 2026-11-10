from pathlib import Path

from chunking import (
    build_records,
    chunk_markdown,
    infer_module_topic,
    split_large_section,
    split_sections,
)


def test_split_sections_splits_on_h2_headings():
    text = "# Título\n\nIntro.\n\n## Uno\ncontenido uno\n\n## Dos\ncontenido dos\n"
    sections = split_sections(text)
    # A primeira seção agrupa o título `#` + preâmbulo; depois uma por cada `##`.
    assert len(sections) == 3
    assert sections[0] == "# Título\n\nIntro."
    assert sections[1].startswith("## Uno")
    assert sections[2].startswith("## Dos")


def test_split_sections_does_not_split_headings_inside_fenced_code():
    text = "# Título\n\n## Real\n```md\n## Esto no es un heading real\n```\nresto\n"
    sections = split_sections(text)
    # Só 2 seções reais (preâmbulo + "## Real"): o heading dentro do
    # fence não deve gerar uma terceira seção.
    assert len(sections) == 2
    assert "## Esto no es un heading real" in sections[1]


def test_split_large_section_bounds_oversized_fence_and_line():
    code_block = "```python\n" + "\n".join(f"x{i} = {i}" for i in range(50)) + "\n```"
    section = "## Grande\n\n" + code_block + "\n\n" + ("párrafo largo. " * 100)
    chunks = split_large_section(section, max_chars=200)
    assert max(map(len, chunks)) <= 200
    assert all("## Grande" in chunk for chunk in chunks)
    assert any("x49 = 49" in chunk for chunk in chunks)


def test_split_large_section_returns_input_unchanged_when_small_enough():
    section = "## Chica\ncontenido corto"
    assert split_large_section(section, max_chars=1000) == [section]


def test_split_large_section_applies_overlap_on_forced_paragraph_split():
    section = "## Grande\n\n" + "\n\n".join(f"Párrafo número {i} con texto de relleno." for i in range(20))
    chunks = split_large_section(section, max_chars=150, overlap=30)
    assert len(chunks) > 1
    # cada chunk (exceto o primeiro) deve conservar uma porção do final do anterior
    for prev, curr in zip(chunks, chunks[1:]):
        assert prev[-10:] in curr


def test_split_large_section_without_overlap_does_not_repeat_tail():
    section = "## Grande\n\n" + "\n\n".join(f"Párrafo número {i} con texto de relleno." for i in range(20))
    chunks = split_large_section(section, max_chars=150, overlap=0)
    assert len(chunks) > 1


def test_chunk_markdown_returns_chunk_text_and_section():
    text = "# Doc\n\n## Sección A\ncontenido A\n"
    chunks = chunk_markdown(text)
    assert chunks == [
        {"chunk_text": "# Doc", "section": "Doc"},
        {"chunk_text": "## Sección A\ncontenido A", "section": "Sección A"},
    ]


def test_infer_module_topic_from_two_level_path(tmp_path):
    root = tmp_path / "knowledge"
    path = root / "REACT_INICIO" / "Estado_Hooks" / "archivo.md"
    module, topic = infer_module_topic(path, root)
    assert module == "react_inicio"
    assert topic == "estado_hooks"


def test_infer_module_topic_from_one_level_path(tmp_path):
    root = tmp_path / "knowledge"
    path = root / "HTML_CSS" / "index.md"
    module, topic = infer_module_topic(path, root)
    assert module == "html_css"
    assert topic is None


def test_build_records_includes_metadata(tmp_path):
    root = tmp_path / "knowledge"
    (root / "BACKEND_NODE" / "Express_Fundamentos").mkdir(parents=True)
    (root / "BACKEND_NODE" / "Express_Fundamentos" / "intro.md").write_text(
        "# Intro\n\n## Qué es Express\ncontenido\n", encoding="utf-8"
    )
    records = build_records(root)
    # "# Intro" (preâmbulo) + "## Qué es Express" -> 2 chunks
    assert len(records) == 2
    record = records[1]
    assert record["source"] == "BACKEND_NODE/Express_Fundamentos/intro.md"
    assert record["chunk_id"] == 1
    assert record["module"] == "backend_node"
    assert record["topic"] == "express_fundamentos"
    assert record["section"] == "Qué es Express"


def test_ids_are_stable_and_distinct_for_old_slug_collisions(tmp_path):
    for name in ("M/T/A.md", "M/T/a.md", "M/T/a__b.md", "M/T/a/b.md"):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Título\nContenido", encoding="utf-8")
    first = build_records(tmp_path)
    assert first == build_records(tmp_path)
    assert len({item["_id"] for item in first}) == 4


def test_tilde_fence_hides_heading():
    assert len(split_sections("## Título\n~~~md\n## exemplo\n~~~\n## Final\ntexto")) == 2
