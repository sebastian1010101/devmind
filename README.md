# DevMind

DevMind é um assistente de estudos de programação. Em vez de procurar manualmente em várias anotações, você faz uma pergunta em linguagem natural e recebe uma explicação com o arquivo, a seção e um trecho de cada fonte citada. Quando a base não sustenta uma resposta, o chat sinaliza a falta de evidência.

## O que você pode fazer

- Conversar com o assistente em um chat responsivo, testar perguntas sugeridas e limpar o histórico da sessão.
- Expandir as fontes para conferir o caminho, a seção e o trecho do Markdown.
- Navegar pelo Guia e restringir uma pergunta a um módulo, tema ou documento.
- Indexar arquivos Markdown em lotes e atualizar a base sem multiplicar os mesmos fragmentos.
- Medir recuperação, abstensão, atribuição de fontes, latência e erros com o mesmo pipeline do chat.

## Arquitetura

```mermaid
flowchart LR
    MD[Markdown] --> CH[Validação e fragmentação]
    CH --> PC[Pinecone · embeddings integrados]
    UI[Next.js · Chat e Guia] --> API[FastAPI]
    API --> R[RAG compartilhado]
    CLI[CLI e avaliação] --> R
    R -->|Consulta e metadados| PC
    R -->|Pergunta e evidência limitada| AI[OpenAI]
    AI -->|Resposta e IDs de evidência| R
    R -->|Validação das citações| API
```

Python 3.12, FastAPI, Pinecone com `llama-text-embed-v2`, OpenAI Chat Completions, pytest, Next.js, React, TypeScript e Tailwind CSS. A visualização em Three.js é decorativa.

## Executar localmente

Instale Python 3.12, uv e Node.js 20.9 ou superior. A verificação usou Node.js 20.20.2. Execute da raiz do repositório. [Instalação do uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
uv venv --python 3.12 .venv
uv pip install -p .venv/bin/python -r requirements.txt
npm --prefix frontend ci
.venv/bin/python ingest.py --module devmind --dry-run
```

Para usar o chat com provedores reais, copie `.env.example` para `.env` se ainda não existir. Preencha `PINECONE_API_KEY` e `OPENAI_API_KEY` no arquivo local. Configure `PINECONE_NAMESPACE=devmind-portfolio` para isolar a demonstração. Use o mesmo namespace em ingestão, API, CLI e avaliação.

Com autorização para consumo no projeto dos provedores, execute os comandos abaixo. `main.py` verifica o índice e cria um índice serverless se ele ainda não existir. Você pode pular esse comando quando já houver um índice compatível.

```bash
.venv/bin/python main.py
.venv/bin/python ingest.py --module devmind
.venv/bin/python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Em outro terminal, execute `npm --prefix frontend run dev` e abra [localhost:3035](http://localhost:3035). A URL padrão do backend é `http://localhost:8000`. Para alterá-la, use `NEXT_PUBLIC_API_URL` em `frontend/.env.local`. Reinicie o servidor após alterar a configuração. Para a demo de produção, use os comandos verificados abaixo.

```bash
npm --prefix frontend run build -- --webpack
npm --prefix frontend run start -- --hostname 127.0.0.1 --port 3035
```

Sem credenciais, os mesmos servidores permitem abrir a interface, consultar `/health`, `/stats` e navegar no Guia. A ação de perguntar retorna uma mensagem de configuração. Para uma consulta pelo terminal, use `.venv/bin/python search.py --debug`.

### Configuração do backend

| Variável | Padrão | Função |
| --- | --- | --- |
| `PINECONE_INDEX_NAME` | `kenzie-knowledge` | Índice integrado com mapeamento `text → chunk_text`. |
| `PINECONE_NAMESPACE` | `devmind` | Partição consultada e atualizada pelo app. |
| `RAG_TOP_K` | `3` | Número máximo de candidatos para o contexto, de 1 a 20. |
| `RAG_SCORE_THRESHOLD` | `0.40` | Limiar inicial de similaridade. Use o conjunto de avaliação para calibrá-lo. |
| `RAG_MODEL` | `gpt-4o` | Modelo Chat Completions com suporte a JSON Schema estrito. |
| `RAG_TEMPERATURE` | Omitida | Valor entre 0 e 2. Defina somente para modelos que aceitam o parâmetro. |
| `RAG_CONTEXT_CHARS` | `10000` | Limite em caracteres do JSON de evidências. |
| `RAG_TIMEOUT_SECONDS` | `15` | Timeout por operação nos SDKs. |
| `FRONTEND_ORIGIN` | localhost e 127.0.0.1 na porta 3035 | Origens CORS, separadas por vírgulas. |

### Atualizar a base

Adicione Markdown UTF-8 em `knowledge/<MÓDULO>/<TEMA>/`, com título e seções `##`. O índice recebe o caminho relativo, a seção e o número de fragmento. Um upsert substitui registros com os mesmos IDs. Para eliminar fragmentos de documentos removidos ou encurtados, execute `.venv/bin/python ingest.py --module devmind --prune`. O comando envia todos os lotes antes de apagar IDs obsoletos do módulo. Aguarde a atualização do índice antes de consultar e execute uma ingestão por vez em cada namespace. [Consistência de dados no Pinecone](https://docs.pinecone.io/guides/data/check-data-freshness)

O módulo `knowledge/DEVMIND` contém exemplos autorais com referências primárias. O catálogo local inclui também o corpus herdado. Confirme a licença e a procedência desse conteúdo antes de incluí-lo em uma distribuição pública. Ao migrar de uma carga antiga, faça o primeiro upsert em um namespace novo para evitar misturar IDs e caminhos antigos.

### Roteiro para a demo

| Pergunta | O que conferir |
| --- | --- |
| Como retiro README.md do staging mantendo minhas edições? | Citação de Git e preservação das alterações locais. |
| Como conto ocorrências em Python com um dicionário e get? | Citação de Python e valor padrão de uma chave ausente. |
| Por que repetir um PUT pode ser seguro e repetir um POST pode duplicar pedidos? | Citação de HTTP e distinção entre os efeitos pretendidos. |
| Qual deles devo usar no meu projeto? | Abstensão ou pedido de especificação pela falta de contexto. |
| Qual é a receita de uma pizza margherita? | Abstensão por falta de evidência. |

## Interface

As capturas mostram o build local. A resposta de Git exibida no desktop usa um provedor simulado.

![Chat com uma seção citada expandida](docs/screenshots/chat-desktop.png)

![Tela inicial do chat em um celular](docs/screenshots/chat-mobile.png)

## Verificação e avaliação

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/python evaluation/evaluate.py
npm --prefix frontend run lint
(cd frontend && npx tsc --noEmit)
npm --prefix frontend run build -- --webpack
```

A [execução simulada](evaluation/results-mock.json) verificou o comportamento do pipeline em 41 cenários. Os simuladores usam os rótulos para construir a recuperação e a geração, portanto o resultado mede a execução das regras do aplicativo. Para medir os provedores com o corpus autoral já carregado, use `.venv/bin/python evaluation/evaluate.py --live --portfolio`. O comando grava um relatório distinto com configuração e resultados por pergunta. A integração opcional e os resultados desta entrega estão no [relatório de testes](docs/TEST_REPORT.md).

## Limitações e próximos passos

O histórico fica na página e cada pergunta é independente. A validação garante que uma citação existe no contexto enviado ao modelo. Aferir se cada afirmação é sustentada pelo trecho exige revisão humana ou uma metodologia adicional. O catálogo local e o índice remoto têm ciclos de atualização separados. A API foi preparada para execução local e ainda precisa de uma política de acesso e cotas antes de exposição pública.

O primeiro passo após a validação com provedores é calibrar o limiar em perguntas rotuladas e revisar erros de fundamentação. Carga pela interface, feedback e painel de métricas ficam depois da validação do MVP.

[Arquitetura](docs/ARCHITECTURE.md) · [Auditoria inicial](docs/AUDIT.md) · [Decisões](docs/DECISIONS.md) · [Testes e entrega](docs/TEST_REPORT.md)
