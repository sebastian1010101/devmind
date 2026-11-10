from pathlib import Path

from guide import (
    GuideModule,
    build_guide,
    humanize_folder,
)

REAL_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_humanize_folder_replaces_underscores():
    assert humanize_folder("Fundamentos_JS") == "Fundamentos JS"
    assert humanize_folder("SQL_PostgreSQL") == "SQL PostgreSQL"


def test_build_guide_orders_documents_within_section(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "MOD" / "Topico" / "MOD02-10-segundo.md", "# MOD02-10 — Segundo\n\ncontenido\n")
    _write(root / "MOD" / "Topico" / "MOD02-05-primero.md", "# MOD02-05 — Primero\n\ncontenido\n")

    modules = build_guide(root)
    assert len(modules) == 1
    section = modules[0].sections[0]
    assert [d.title for d in section.documents] == ["Primero", "Segundo"]


def test_build_guide_derives_module_order_from_index(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "SEGUNDO" / "index.md", "# 02. Segundo Módulo — Índice\n")
    _write(root / "SEGUNDO" / "Tema" / "MOD02-01-doc.md", "# MOD02-01 — Doc\n\ncontenido\n")
    _write(root / "PRIMERO" / "index.md", "# 01. Primer Módulo — Índice\n")
    _write(root / "PRIMERO" / "Tema" / "MOD01-01-doc.md", "# MOD01-01 — Doc\n\ncontenido\n")

    modules = build_guide(root)
    assert [m.id for m in modules] == ["primero", "segundo"]
    assert modules[0].title == "Primer Módulo"
    assert modules[0].order == 1.0
    assert modules[1].order == 2.0


def test_build_guide_skips_documents_without_topic(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "MOD" / "index.md", "# Mi Módulo — Índice\n")
    _write(root / "MOD" / "suelto.md", "# Suelto\n\ncontenido\n")
    _write(root / "MOD" / "Tema" / "MOD01-01-doc.md", "# MOD01-01 — Doc\n\ncontenido\n")

    modules = build_guide(root)
    assert len(modules) == 1
    assert len(modules[0].sections) == 1
    assert sum(len(s.documents) for s in modules[0].sections) == 1


def test_as_dict_shape(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "MOD" / "Tema" / "MOD01-01-doc.md", "# MOD01-01 — Doc\n\ncontenido\n")

    module = build_guide(root)[0]
    data = module.as_dict()
    assert set(data) == {"id", "title", "order", "sections"}
    assert set(data["sections"][0]) == {"id", "title", "order", "documents"}
    assert set(data["sections"][0]["documents"][0]) == {"id", "title", "source", "order", "topic"}


def test_build_guide_against_real_knowledge_base_has_eight_modules_in_order():
    modules = build_guide(REAL_KNOWLEDGE_DIR)
    assert [m.order for m in modules] == list(range(1, 9))
    for module in modules:
        assert isinstance(module, GuideModule)
        assert module.sections, f"{module.id} no tiene secciones"
        for section in module.sections:
            assert section.documents, f"{module.id}/{section.id} no tiene documentos"
            orders = [d.order for d in section.documents]
            assert orders == sorted(orders)
