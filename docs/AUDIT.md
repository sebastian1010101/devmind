# Auditoría inicial de DevMind

Inspección del árbol local el 10 de noviembre de 2026. El árbol de trabajo ya contenía cambios y archivos sin seguimiento sobre `35e654e`. Esta auditoría describe ese árbol, incluidos los cambios previos del usuario.

| Área | Estado inicial | Hallazgo |
| --- | --- | --- |
| Corpus y fragmentación | Implementado localmente | 495 Markdown en siete módulos. El máximo declarado podía superarse con líneas y bloques de código largos o al añadir solapamiento y encabezados. Algunos documentos mencionan Kenzie Academy y la procedencia y licencia del corpus heredado requieren confirmación antes de una publicación. |
| Ingestión | Parcial | `main.py` configura un índice con embeddings integrados `llama-text-embed-v2`. `ingest.py` hacía upsert en lotes, volvía a leer y fragmentar el corpus después de calcular estadísticas y podía abortar con un archivo ilegible. Los identificadores podían colisionar al normalizar rutas. El borrado completo previo a reingestar dejaba el índice expuesto a cargas parciales. |
| Recuperación | Parcial | CLI, FastAPI y evaluación comparten `rag.py`. Recupera por texto, filtra por similitud y admite alcance por módulo o tema. La CLI repetía la consulta en modo debug y el frontend enviaba su propio top-k fijo. |
| Generación y fuentes | Parcial | El prompt pedía respuestas fundamentadas pero aceptaba cualquier salida, enviaba contexto sin presupuesto y mostraba todos los documentos recuperados como fuentes. Usar solo el nombre del archivo generaba ambigüedad. Faltaba distinguir la abstención de una respuesta inválida. |
| API y configuración | Parcial | `/health`, `/stats` y `/guide` son locales. `/ask` carecía de límites de entrada y traducción de errores externos. Timeout y reintentos quedaban a criterio de cada SDK. El estado local se confundía con conectividad a Pinecone en el chat. |
| Interfaz | Parcial | Next.js, React, Tailwind, terminal y visualización 3D ya existían. Hay historial en memoria y comandos ASK/GUIDE. Faltaban ejemplos visibles, botón de limpiar y citas con sección disponibles para cualquier usuario. El build falló por la descarga de Geist Mono. |
| Evaluación | Parcial | El árbol local ya había sustituido `eval_rag.py` y `eval_dataset.json` por `evaluation/evaluate.py` y `questions.json`. Medía Hit@K y rechazo por igualdad de texto. Faltaban atribución, latencias, tasa de errores y casos ambiguos. El JSON heredado carecía de la configuración y procedencia necesarias para usarlo como evidencia de esta versión. |
| Pruebas | Parcial | La suite inicial cubría utilidades puras. Faltaban pruebas de contrato del pipeline, proveedores, API e integración real optativa. |
| Credenciales | Parcial | Se detectó configuración local de ambas claves sin mostrar sus valores. `.env` y `frontend/.env.local` están ignorados y no aparecen en el historial Git local. La búsqueda de patrones de claves de los proveedores en el árbol inspeccionado no encontró coincidencias. |

## Línea base ejecutada

- Python 3.12.3, OpenAI SDK 3.11.0, Pinecone SDK 10.0.0, FastAPI 0.121.1 y pytest 8.4.2. `uv pip check` confirmó que las dependencias instaladas eran compatibles.
- `.venv/bin/python -m pytest tests/ -q` pasó con 28 pruebas.
- `.venv/bin/python ingest.py --dry-run` generó 3.824 fragmentos de 495 documentos, sin vacíos, fallos ni duplicados detectados.
- Node 20.20.2, Next.js 16.3.6 y React 19.2.8. ESLint y TypeScript pasaron. El build falló al acceder a Google Fonts.
- La auditoría inicial no consumió Pinecone ni OpenAI. `evaluation/results.json` pertenece al estado previo.
