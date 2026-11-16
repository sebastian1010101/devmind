# Validación real del RAG de DevMind

Ejecución del 12/11/2026. Se comprobó el recorrido Markdown → fragmentación → Pinecone → OpenAI → respuesta con citas y el contrato de `POST /ask` mediante ASGI. La evidencia definitiva corresponde al código de esta entrega sobre el commit base `09d84e2`. El JSON registra modificaciones locales y hashes de los archivos ejecutados. [Evidencia real](../evaluation/results-live-2026-11-12.json)

## Arquitectura y configuración auditadas

| Área | Comprobación |
| --- | --- |
| Chat | `POST /ask` valida preguntas de 1 a 1200 caracteres, `top_k` de 1 a 20 y filtros de módulo, tema y documento. |
| Documentos | `ingest.py` es una CLI. `/guide` y `/guide/document` leen el catálogo y los documentos locales. |
| Evaluación | `evaluation/evaluate.py` comparte `answer_question` con la API y la CLI. El modo predeterminado utiliza mocks y `--live` habilita proveedores. |
| Pipeline | `stats.py` valida el corpus, `chunking.py` produce texto y metadata, Pinecone genera embeddings y `rag.py` construye el contexto y valida la salida. |
| Pinecone real | Índice `kenzie-knowledge`, listo, campo `chunk_text` de tipo `semantic_text`, modelo `llama-text-embed-v2`, métrica `cosine`, dimensiones de lectura y escritura 1024. |
| OpenAI real | Modelo solicitado `gpt-4o`, resuelto como `gpt-4o-2024-08-06`, con Chat Completions y JSON Schema estricto. |
| Parámetros | `top_k=3`, umbral `0.40`, contexto hasta 10000 caracteres serializados, timeout por operación de 15 segundos y salida hasta 1200 tokens. |
| Reintentos | OpenAI tiene `max_retries=0`. Pinecone permite una repetición y espera máxima configurada de 2 segundos. |
| Credenciales | Ambas variables estaban presentes en el backend. `.env` y `frontend/.env.local` están ignorados. El informe conserva configuración pública y métricas. |
| Namespace | La configuración existente apuntaba a `kenzie`. El validador usó `devmind-validation-<uuid>` y restauró la configuración de su proceso al terminar. |

`GET /health` comprueba el proceso. `/stats`, `/guide` y `/guide/document` leen archivos locales. Su éxito se evalúa por separado de la conectividad con los proveedores. La integración real usó claves locales sin imprimir sus valores. [API](../api.py), [Configuración](../config.py), [Proveedores](../providers.py)

La documentación oficial confirma el formato estructurado utilizado y publica las tarifas empleadas en esta estimación. El esquema del índice se obtuvo de la respuesta real de Pinecone mediante `schema.fields`, compatible con el SDK 10 instalado. [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=chat), [GPT-4o](https://developers.openai.com/api/docs/models/gpt-4o)

## Pruebas reales ejecutadas

1. Leer la descripción del índice y consultar el modelo de OpenAI para comprobar autenticación y acceso.
2. Ejecutar el test optativo con un documento sintético y namespace único. Pasó con una respuesta que incluyó el código del documento y citó su fuente.
3. Ejecutar el nuevo validador con los ocho documentos autorales de `knowledge/DEVMIND`, que producen 17 fragmentos y 5703 caracteres de texto por carga.
4. Cargar esos 17 IDs dos veces y listar el namespace hasta comprobar exactamente el mismo conjunto de 17 IDs después de cada carga.
5. Esperar visibilidad de búsqueda y evaluar las once preguntas de portafolio. Se solicitaron cinco candidatos para métricas y se enviaron como máximo los tres elegibles al generador.
6. Enviar dos solicitudes a `/ask` mediante `TestClient`, conservando los clientes reales de ambos proveedores. Git con filtro de documento devolvió 200 y fuente correcta. Pizza devolvió 200 y `insufficient_evidence`.
7. Eliminar exclusivamente los IDs escritos en ese namespace y verificar que su listado quedó vacío.

Se completaron dos ejecuciones del validador, antes y después del ajuste de fundamentación descrito más abajo. Cada una usó un namespace propio y verificó la limpieza. El JSON versionado conserva la segunda. El primer informe completo permanece local en `evaluation/validation-baseline-local.json`.

La prueba de API ejecuta validación, handlers y serialización ASGI en el proceso. La interfaz visual y el transporte por un servidor HTTP independiente quedan fuera de esta ejecución. El corpus completo de 3841 fragmentos fue validado con `--dry-run`.

## Métricas reales definitivas

Inicio registrado a las 20:39:19 UTC, equivalentes a las 17:39:19 en São Paulo. El subconjunto contiene siete preguntas con fuente esperada y cuatro con abstención esperada. [Resultados por pregunta](../evaluation/results-live-2026-11-12.json)

| Métrica | Resultado | Denominador |
| --- | --- | --- |
| Hit@1 | 7/7, 100 % | Preguntas con fuente esperada y recuperación completada. |
| Hit@3 | 7/7, 100 % | Mismo conjunto, primeros tres resultados brutos. |
| Hit@5 | 7/7, 100 % | Mismo conjunto, primeros cinco resultados brutos. |
| Decisión de responder o abstenerse | 11/11, 100 % | Ejecuciones sin error. |
| Rechazo esperado | 4/4, 100 % | Pizza, Netuno y dos preguntas ambiguas. |
| Atribución estructural | 7/7, 100 % | Respuestas cuyas citas pertenecen al contexto, por ruta, sección y ordinal. |
| Fuente esperada citada | 7/7, 100 % | Preguntas positivas que citaron una fuente esperada. |
| Precisión de fuentes etiquetadas | 8/8, 100 % | Referencias cuya ruta figura en las etiquetas. HTML/CSS citó dos secciones. |
| Errores | 0/11, 0 % | Todas las preguntas del subconjunto. |
| Mediana de recuperación | 206,86 ms | 11 búsquedas. |
| Mediana de generación | 1655,80 ms | 7 generaciones. |
| Mediana total | 1614,34 ms | 11 ejecuciones, incluidas cuatro abstenciones locales. |

Hit@K compara rutas en los resultados brutos. La precisión de fuentes usa etiquetas del dataset y puede penalizar fuentes válidas si las etiquetas son incompletas. La atribución estructural comprueba pertenencia al contexto. El soporte de las afirmaciones se revisó además sobre los documentos completos.

El conjunto es pequeño y procede del corpus de la demo. La segunda ejecución reutiliza las preguntas tras un ajuste del prompt. La evaluación con preguntas reservadas y un revisor humano independiente queda pendiente.

## Revisión cualitativa de fundamentación

Revisión realizada por el asistente sobre las siete respuestas definitivas, las citas y los Markdown completos.

| ID | Tema | Afirmaciones comprobadas | Resultado |
| --- | --- | --- | --- |
| 31 | Git | `git restore --staged README.md` modifica staging y conserva ediciones. | Respaldadas por la sección citada. |
| 32 | HTML/CSS | `for`/`id`, `display: flex`, `flex-wrap`, `gap` y crecimiento de elementos. | Respaldadas por dos secciones citadas. |
| 33 | JavaScript | Transformación con `map`, selección con `filter`, nuevo array y callback pura. | Respaldadas por la sección citada. |
| 34 | Python | Contador por clave, `get(item, 0)` e incremento del diccionario. | Respaldadas por el ejemplo y la explicación. |
| 35 | HTTP | Efecto idempotente de PUT, posible duplicación de POST y consulta del contrato antes de reintentar. | Respaldadas en contexto. La redacción final incluye la decisión del contrato. |
| 36 | React | Actualización funcional y copia con spread para agregar un elemento. | Respaldadas por la sección citada. |
| 37 | Autenticación | 401 ante ausencia de credenciales válidas y 403 para una identidad reconocida sin permiso. | Respaldadas por la sección citada. |

La primera respuesta de HTTP afirmó que POST no es idempotente sin conservar el matiz del contrato. El documento explica que su semántica por sí sola no garantiza idempotencia y pide comprobar mecanismos del endpoint. Se ajustó `SYSTEM_PROMPT` para preservar condiciones y garantías de la evidencia. La segunda respuesta incorporó explícitamente la comprobación del contrato tras un timeout.

La revisión del asistente no detectó afirmaciones sin respaldo en las siete respuestas definitivas. Este resultado describe esa revisión puntual. Las pruebas automáticas miden contratos, etiquetas y pertenencia de citas. La revisión humana independiente de matices y calidad pedagógica sigue pendiente.

## Consumo y coste estimado

| Dato medido | Ejecución definitiva |
| --- | --- |
| Entrada OpenAI | 3081 tokens en 7 respuestas de uso. |
| Salida OpenAI | 919 tokens en 7 respuestas de uso. |
| Total OpenAI | 4000 tokens. |
| Entrada cacheada | 0 tokens. |
| Embedding de consultas Pinecone | 184 tokens en 11 búsquedas. |
| Lecturas Pinecone | 11 unidades en esas búsquedas. |
| Ingestión | 5703 caracteres por pasada, dos pasadas de 17 fragmentos. |

Con las tarifas publicadas de GPT-4o de USD 2,50 por millón de tokens de entrada y USD 10 por millón de salida, las siete generaciones medidas cuestan aproximadamente `(3081 × 2,50 + 919 × 10) / 1000000 = USD 0,0168925`. La medición previa registró 2843 tokens de entrada y 904 de salida, equivalentes a USD 0,0161475. Ambas evaluaciones suman aproximadamente USD 0,03304 de generación medida. [Tarifas de GPT-4o](https://developers.openai.com/api/docs/models/gpt-4o)

La estimación cubre las filas evaluadas. El test sintético, las consultas adicionales de API, los sondeos, la ingestión y la limpieza tienen consumo adicional. El endpoint actual no expone trazas de tokens. El upsert del SDK informa cantidad de registros, sin tokens de ingestión. El coste monetario total de la sesión y la factura de Pinecone quedan pendientes de contrastar con los paneles de los proveedores.

La carga real se mantuvo acotada al corpus autoral. Estimar la ingestión completa requiere el tokenizer y las tarifas aplicables al modelo y al proyecto, además de unidades de escritura y almacenamiento. Los 3841 fragmentos completos permanecen fuera de las cargas reales de esta sesión.

## Mocks y pruebas de errores

El evaluador en modo mock ejecutó 41 preguntas. Obtuvo Hit@1/3/5 de 32/32, decisiones correctas de 41/41, rechazo de 9/9, atribución de 32/32 y cero errores. Las fixtures construyen respuestas a partir de las etiquetas. El consumo sin respuesta de uso queda en `null` en el agregado, con cero muestras. [Evaluador](../evaluation/evaluate.py)

La suite local ejecutó casos de configuración ausente, 401, 403, 404, 402, 429, error 500, timeout, JSON inválido, citas ajenas al contexto y finalización truncada. Verificó mensajes públicos controlados y ausencia del cuerpo privado del proveedor en los logs. Esos errores se inyectaron mediante mocks. Las llamadas iniciales en el sandbox fallaron realmente por conexión y se tradujeron a `provider_error`/502. Con acceso de red permitido, ambos proveedores respondieron.

## Correcciones y archivos de esta entrega

| Archivo | Cambio |
| --- | --- |
| `rag.py` | Uso de Pinecone, tokens OpenAI y modelo resuelto en `RunTrace`, incluso al rechazar una salida facturable. Prompt que conserva matices. |
| `evaluation/evaluate.py` | Precisión de fuentes etiquetadas, consumo con cantidad de muestras y selección explícita de namespace. |
| `evaluation/validate_live.py` | Esquema, autenticación, ingestión aislada, reingestión, evaluación, API, limpieza y evidencia con hashes. |
| `tests/test_rag_pipeline.py` | Consumo tras salida inválida y traducción de errores de autenticación, configuración, saldo y proveedor. |
| `tests/test_evaluate_metrics.py` | Precisión por referencia frente a éxito por pregunta, y consumo desconocido frente a cero medido. |
| `tests/test_validate_live.py` | Limpieza de IDs propios tras fallo parcial y restauración del namespace. |
| `evaluation/results-live-2026-11-12.json` | Evidencia real, respuestas, métricas, configuración pública, hashes y limpieza. |
| `docs/TEST_REPORT.md` | Estado verificado actualizado sobre el registro histórico. |
| `docs/ACTIVE_RECALL_PLAN.md` | Diseño de tarjetas, corrección, persistencia, repasos y preguntas diarias. |

La suite ampliada pasó con 84 pruebas y una integración real omitida en esa ejecución local. La integración real pasó separadamente con una prueba. ESLint, TypeScript, build Webpack e `ingest.py --dry-run` también pasaron. El aviso de pytest procede del alias `anyio.abc.BlockingPortal` usado por Starlette.

También se probó `npm run build` con Turbopack. Falló al intentar abrir un puerto interno con `Operation not permitted`, incluso con ejecución escalada. El build reproducible en este entorno usa `npm run build -- --webpack`, como ya indica el README. `uv pip check` confirmó compatibilidad de los 34 paquetes instalados. La ejecución utilizó Python 3.14.4, registrado en la evidencia.

## Reproducción desde la raíz

Preparar el entorno con `uv` según `AGENTS.md`. Configurar `PINECONE_API_KEY` y `OPENAI_API_KEY` en `.env`, con acceso al índice integrado descrito. El validador selecciona un namespace único.

```bash
DEVMIND_ALLOW_LIVE=0 .venv/bin/python -m pytest tests/ -q
.venv/bin/python ingest.py --dry-run
.venv/bin/python evaluation/evaluate.py --output evaluation/results-mock-local.json
DEVMIND_ALLOW_LIVE=1 .venv/bin/python -m pytest tests/test_live_integration.py -m integration -q
.venv/bin/python evaluation/validate_live.py --live
npm --prefix frontend run lint
(cd frontend && npx --no-install tsc --noEmit)
npm --prefix frontend run build -- --webpack
```

El comando real genera por defecto `evaluation/validation-real-local.json`, ignorado por Git. Devuelve un estado distinto de cero ante errores, decisiones incorrectas, fuentes esperadas ausentes, fallos de API o limpieza sin verificar. Si la limpieza falla, el informe conserva namespace y datos de la carga para retirar esos IDs y repetir su verificación.

Para evaluar un namespace ya cargado, el evaluador admite `--live --portfolio --namespace NOMBRE`. Esa variante consulta los registros existentes. El validador completo realiza y limpia su propia carga.

## Pendientes para la candidatura

- Revisar respuestas con una persona y ampliar la evaluación con preguntas reservadas y garantías condicionales.
- Preparar una demo visible del chat contra un namespace persistente. Los namespaces de esta validación se limpiaron.
- Comprobar la configuración del namespace al presentar la demo y documentar la actualización del catálogo local y del índice remoto.
- Implementar Active Recall según el plan y registrar sus pruebas antes de presentarlo como funcional.
- Resolver identidad, permisos y cotas si se decide publicar el servicio.

## Preguntas técnicas de entrevista

### ¿Dónde se generan los embeddings y cómo se comprueba su compatibilidad?

Pinecone genera embeddings de documentos y consultas con el modelo integrado. El índice real expone `chunk_text`, `llama-text-embed-v2` y dimensiones 1024 para lectura y escritura. El validador inspecciona el esquema antes de escribir y rechaza una configuración incompatible. [Ingestión](../ingest.py), [Validación](../evaluation/validate_live.py)

### ¿Cómo se impide que el modelo cite un documento inventado?

`build_context` asigna IDs locales a los fragmentos elegibles. OpenAI devuelve texto e IDs mediante una salida estructurada. `_generate` rechaza IDs ausentes del mapa y obtiene las fuentes de la metadata recuperada. La revisión semántica comprueba además si el fragmento respalda cada afirmación. [Generación y citas](../rag.py)

### ¿Por qué una reingestión mantiene la cantidad de registros?

`document_records` deriva cada ID del módulo, hash de ruta y ordinal del fragmento. Reingestar el mismo contenido produce los mismos IDs y el upsert los reemplaza. La prueba real verificó 17 IDs después de dos cargas. `--prune` elimina fragmentos obsoletos después de completar los upserts. [Fragmentación](../chunking.py), [Upsert](../ingest.py)

### ¿Cómo decide DevMind abstenerse y cómo se mide?

El pipeline filtra por umbral y presupuesto de contexto. Sin evidencia elegible devuelve `insufficient_evidence` localmente. Con evidencia, el modelo puede devolver `answer=null` y citas vacías. El evaluador compara la decisión con `should_answer`. Las siete respuestas y cuatro abstenciones reales coincidieron con las etiquetas. [Pipeline](../rag.py), [Métricas](../evaluation/evaluate.py)

### ¿Cómo se distinguen fallos de proveedores y resultados del RAG?

`provider_errors` convierte fallos externos en `ServiceError` con código y HTTP controlados. `RunTrace` registra fases, uso y modelo. El evaluador distingue errores de abstenciones, conserva recuperación completada aunque falle la generación y deja sin valor las métricas sin muestras. Los mocks verifican contratos y `live` registra acceso real. [Errores](../providers.py), [Trazas](../rag.py), [Evaluador](../evaluation/evaluate.py)
