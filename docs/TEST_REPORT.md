# Relatório de verificação

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
