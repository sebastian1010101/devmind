# Decisões técnicas

| Decisão | Motivo e consequência |
| --- | --- |
| Manter Next.js e FastAPI | O chat, o Guia, os comandos e a integração já existiam. A melhoria aproveita o código e mantém a API acessível à CLI. A execução local usa dois processos. |
| Usar fontes tipográficas do sistema | O build anterior buscava Geist Mono no Google Fonts. A mudança elimina essa dependência de build e preserva a fonte monoespaçada para os detalhes técnicos. |
| Manter embeddings integrados | Pinecone faz embedding de documentos e consultas no mesmo índice. O app mantém apenas a configuração do modelo, o esquema de metadata e o fluxo de upsert. |
| Usar um namespace novo e IDs estáveis | Os IDs antigos e fontes por nome de arquivo podem permanecer no namespace histórico. Iniciar em `devmind` isola o formato atualizado. A leitura de um namespace legado ainda é possível com configuração explícita. O escopo de documento por caminho requer reingestão. |
| Carregar antes de remover | A limpeza só é executada após todos os upserts. O processo não é transacional e deve ter um escritor por namespace. Cargas simultâneas ou uma réplica local desatualizada podem produzir um conjunto remoto incoerente. |
| Validar citações com IDs locais | O modelo recebe texto e IDs temporários. A API resolve os IDs e mostra a evidência. A validação é estrutural e complementa a revisão semântica. |
| Preservar `gpt-4o` com override | É o modelo da configuração original e suporta a saída estruturada usada aqui. OpenAI anunciou a retirada dos snapshots documentados em 14/01/2027. Use `RAG_MODEL` para testar a substituição antes de migrar. [OpenAI Deprecations](https://developers.openai.com/api/docs/deprecations) |
| Separar corpus autoral e herdado | Os sete novos guias permitem reproduzir a demo com poucos registros e fontes revisáveis. O corpus herdado permanece no diretório existente e pode ser incluído em execuções locais autorizadas. |
| Separar avaliações simuladas e reais | O modo simulado verifica o fluxo e as métricas com entrada controlada. O modo real mede o comportamento do índice e do modelo configurados e exige opt-in. |
