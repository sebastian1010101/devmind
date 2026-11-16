# Relatório de verificação

## Active Recall implementado em 12/11/2026

O modo Estudo acrescenta flashcards com evidência RAG, avaliação por conceitos, SQLite, autoavaliação, calendário determinista, sessão diária idempotente e progresso. A validação final passou com 143 testes locais e uma integração RAG optativa omitida, incluindo 59 novos testes de Active Recall. ESLint, TypeScript, build Webpack e dry-run do corpus passaram.

Uma prova controlada com Pinecone e OpenAI gerou um cartão e avaliou três respostas sintéticas, verificando replay, calendário, persistência e limpeza do namespace. O Chrome verificou geração, falha e recuperação de resposta, avaliação, fontes, autoavaliação e progresso em desktop e celular com provedores simulados. A revisão detectou uma imprecisão na explicação real; a implementação final usa explicação extrativa, verificada também por replay. O relatório registra falsos positivos possíveis da guarda conservadora; não se afirma validação pedagógica completa. [Entrega e limites](ACTIVE_RECALL_REPORT.md), [operação](ACTIVE_RECALL.md), [evidência real](../evaluation/learning-live-2026-11-12.json), [navegador](../evaluation/learning-browser-2026-11-12.json).

O Turbopack voltou a falhar ao abrir uma porta interna, inclusive na repetição escalada. A produção foi validada com `npm run build -- --webpack`. As notas anteriores ficam preservadas abaixo.

## Atualização verificada em 12/11/2026

A integração real com Pinecone e OpenAI foi executada nesta entrega. O teste sintético passou e duas execuções com o corpus autoral verificaram autenticação, esquema de embeddings, ingestão, recuperação, geração, citações, abstensão, reingestão com 17 IDs e limpeza do namespace isolado. O validador também confirmou duas respostas de `POST /ask` por ASGI com os clientes reais.

Na execução definitiva, Hit@1/3/5 foi 7/7, a decisão de responder ou abster foi correta em 11/11 casos, a atribuição estrutural foi 7/7 e a precisão das referências etiquetadas foi 8/8. Houve zero erros. A revisão qualitativa do assistente sobre os sete documentos e respostas está registrada separadamente das métricas automáticas. [Relatório atual](RAG_EVALUATION.md), [Evidência real](../evaluation/results-live-2026-11-12.json)

As verificações locais ampliadas passaram com 84 testes e uma integração omitida nessa execução, ESLint, TypeScript, build de produção com Webpack e dry-run de 503 documentos e 3841 fragmentos. A integração real optativa passou separadamente com um teste. O desenho da próxima funcionalidade está no plano de Active Recall. [Plano](ACTIVE_RECALL_PLAN.md)

O build padrão com Turbopack foi tentado e falhou com `Operation not permitted` ao abrir uma porta interna, inclusive fora do sandbox. O comando verificado para este ambiente continua sendo `npm run build -- --webpack`. `uv pip check` confirmou os 34 pacotes instalados compatíveis, com Python 3.14.4.

## Registro histórico de 10/11/2026

As seções seguintes preservam o registro anterior, inclusive os bloqueios e pendências existentes naquela data. O estado vigente é o da atualização acima.

Execução local em 10 de novembro de 2026. As credenciais estavam configuradas localmente. O ensaio com provedores reais exige autorização de consumo e ficou pendente.

## Testes executados

| Comando ou ensaio | Resultado |
| --- | --- |
| `DEVMIND_ALLOW_LIVE=0 .venv/bin/python -m pytest tests/ -q` | 59 passaram, 1 integração real omitida. O TestClient de Starlette emite um aviso de depreciação de um alias do AnyIO. |
| `.venv/bin/python ingest.py --dry-run` | 503 documentos válidos e 3.841 fragmentos. Zero arquivos inválidos, vazios ou potencialmente duplicados. |
| `.venv/bin/python ingest.py --module devmind --dry-run` | 8 documentos válidos e 17 fragmentos. |
| `UV_CACHE_DIR=/tmp/devmind-uv uv pip check -p .venv/bin/python` | 39 pacotes instalados compatíveis. |
| `npm ci --dry-run --offline --ignore-scripts` em diretório temporário | O npm aceitou o lockfile e resolveu a instalação simulada. |
| `npm --prefix frontend run lint` e `(cd frontend && npx tsc --noEmit)` | ESLint e TypeScript passaram. |
| `npm --prefix frontend run build -- --webpack` | Build de produção e prerender da rota principal passaram. A execução padrão com Turbopack encontrou uma restrição de bind de porta interna neste ambiente. |
| Chrome com Next.js de produção e FastAPI local | Confirmou catálogo, Guia, erro de credenciais reais ausentes, exemplos, indicador de carga, histórico, abertura das fontes e limpeza. O navegador recebeu fixtures para os cenários de resposta e abstensão. Em 390 × 844, a tela inicial coube sem rolagem horizontal. |

A prova `test_markdown_to_api_answer_with_mock_providers` executa Markdown → fragmentação → upsert idempotente → recuperação → geração → `POST /ask`. Para repeti-la isoladamente:

```bash
.venv/bin/python -m pytest tests/test_api.py -k markdown_to_api -q
```

As capturas em [desktop](screenshots/chat-desktop.png) e [celular](screenshots/chat-mobile.png) são desse ensaio no navegador. O build e os testes usaram as dependências já instaladas.

## Avaliação RAG

O comando `.venv/bin/python evaluation/evaluate.py --output evaluation/results-mock.json` executou 41 perguntas, incluindo 32 com fontes esperadas e 9 com abstensão esperada. A seleção `--portfolio` também foi executada separadamente em modo mock com 11 perguntas. O [JSON da execução completa](../evaluation/results-mock.json) guarda timestamp, hash do dataset, configuração e registros por pergunta.

| Métrica | Resultado com mocks |
| --- | --- |
| Retrieval Hit@1, @3 e @5 | 32/32 em cada corte |
| Acurácia de abstensão | 41/41 |
| Rejeições esperadas | 9/9 |
| Atribuição estrutural | 32/32 respostas |
| Fonte esperada citada | 32/32 |
| Erros | 0/41 |
| Mediana de recuperação | 0,02 ms em 41 chamadas simuladas |
| Mediana de geração | 0,15 ms em 34 chamadas simuladas |
| Mediana total | 0,18 ms em 41 execuções |

As fixtures usam os rótulos para construir os resultados. Os números verificam os caminhos do aplicativo e o cálculo das métricas. Qualidade semântica, latência dos provedores e suporte de cada afirmação precisam de medições reais e revisão. O arquivo `evaluation/results.json` já existia e registra uma versão anterior com configuração diferente. Ele ficou fora dos resultados desta entrega.

## Validar com provedores reais

Configure as duas chaves em `.env`, aponte `PINECONE_INDEX_NAME` para um índice serverless integrado compatível e use um namespace dedicado, como `devmind-portfolio`. Com autorização de consumo:

```bash
.venv/bin/python ingest.py --module devmind
DEVMIND_ALLOW_LIVE=1 .venv/bin/python -m pytest tests/test_live_integration.py -m integration -q
.venv/bin/python evaluation/evaluate.py --live --portfolio
```

A integração envia um documento sintético para um namespace único, aguarda sua visibilidade, verifica a resposta e remove os registros de teste. A avaliação consulta o namespace de portfólio e salva `evaluation/results-real-local.json`. Após a ingestão, aguarde a propagação dos registros antes de executar a avaliação. Execute então o roteiro de cinco perguntas do [README](../README.md#roteiro-para-a-demo) no navegador e confira a pertinência de cada citação.

## Aceitação

- [x] A interface, os endpoints locais e o fluxo Markdown → resposta simulada foram executados.
- [x] A validação, a geração de IDs, a deduplicação por upsert e a limpeza foram verificadas com testes.
- [x] O teste automatizado e o relatório de avaliação simulada são reproduzíveis.
- [x] As variáveis com chaves ficaram locais e os arquivos correspondentes estão ignorados pelo Git.
- [ ] Confirmar a indexação e a recuperação reais no Pinecone com o corpus autoral.
- [ ] Confirmar respostas fundamentadas, fontes pertinentes e abstensão com OpenAI real.
- [ ] Executar e revisar a avaliação real e a demo no navegador com os dois provedores.

## Sequência de entrega

| Data de referência | Etapa |
| --- | --- |
| 10/11 | Auditoria e linha base |
| 11/11 | Ingestão, recuperação e geração |
| 12/11 | Citações, abstensão, limites e erros |
| 13/11 | Chat e Guia |
| 14/11 | Dataset, avaliação e testes |
| 15/11 | Documentação e capturas |
| 16/11 | Validação real e revisão da demo |
| 17/11 | Revisão final do material de portfólio |

As etapas locais foram antecipadas nesta sessão. A validação real depende da autorização indicada acima.
