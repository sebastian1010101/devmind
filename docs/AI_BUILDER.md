# DevMind — material para candidatura AI Builder

## Cinco perguntas técnicas de entrevista

1. **Como impedir que reenvios avancem duas vezes a revisão?** `LearningStore.claim` reserva uma chave única por estudante, operação e UUID; o fingerprint detecta mudanças de parâmetros. `_reservation` verifica o token do lease. `save_review` grava evento e calendário na mesma transação. Uma repetição concluída retorna o resultado persistido. Cobrança externa exatamente uma vez continua fora dessa garantia.
2. **Por que guardar o texto do fragmento se já há um ID no Pinecone?** O ID deriva da rota e do ordinal e pode sobreviver a edições. `card_evidence` guarda texto e SHA-256, índice e namespace. A avaliação usa essa versão, e a API sinaliza alterações no documento atual. Citações existentes ainda precisam de revisão semântica.
3. **Como a avaliação aceita respostas com outras palavras?** O avaliador recebe pergunta, conceitos esperados, referência e evidências salvas, com saída JSON Schema estrita. O prompt pede equivalência semântica e ignora diferenças superficiais. O backend verifica estrutura, citações e inconsistências como `correct` com conceitos ausentes. `ungradable` e autoavaliação reconhecem a falibilidade do modelo.
4. **Como separar IA de decisões deterministas?** A IA gera questões e avalia conceitos. `review_schedule.advance` calcula intervalos e datas sem rede. A escolha diária usa SQL, data local e chave única de sessão. Essas regras têm testes com relógio controlado, incluindo a virada do dia em São Paulo.
5. **O que precisaria mudar para publicar para vários estudantes?** Identidade autenticada, autorização por cartão/tentativa, isolamento por usuário e cotas por identidade precisam substituir o estudante fixo da demo. A guarda local não é autenticação. Concorrência de escrita maior e múltiplas instâncias também justificariam migrar SQLite para PostgreSQL e revisar leases, backups e observabilidade.

## Descrição para CV ATS em português brasileiro

**DevMind — Agente de aprendizagem com IA generativa:** desenvolvi uma aplicação full stack com Python, FastAPI, Next.js, React e TypeScript, integrando RAG com Pinecone e OpenAI para gerar flashcards fundamentados em documentos e avaliar respostas por conceitos. Implementei saídas estruturadas com JSON Schema e Pydantic, evidências versionadas com SHA-256, persistência e migrações SQLite, idempotência transacional, recuperação após falhas de provedores, repetição espaçada determinista, sessões diárias e acompanhamento de progresso. Validei o fluxo com pytest, testes de interface em Chrome e uma prova controlada com provedores reais. MVP demonstrável localmente para um estudante.

Use as contagens e medições do [relatório de entrega](ACTIVE_RECALL_REPORT.md) ao adaptar o CV. Não apresente a prova pequena como medida de qualidade geral, uma avaliação humana independente ou uma plataforma multiusuário pronta para produção.
