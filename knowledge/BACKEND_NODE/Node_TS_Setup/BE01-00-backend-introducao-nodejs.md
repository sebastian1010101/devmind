# BE01-00 — Backend: Introdução e o que é Node.js

## O que é Backend

A parte da aplicação que **roda no servidor** — invisível pro usuário:

```text
Frontend (navegador)  →  HTTP request  →  Backend (servidor)
                                              │
                                              ├── regras de negócio
                                              ├── autenticação
                                              ├── banco de dados
                                              └── resposta (JSON)
```

O que o backend faz:

- **Regras de negócio** — cálculos, validações, lógica da aplicação
- **Persistência** — salva e lê dados do banco
- **Segurança** — senhas, tokens, permissões (não confie no frontend)
- **Integrações** — pagamentos, e-mails, APIs externas

## O que é Node.js

Um **runtime JavaScript** — permite rodar JS fora do navegador, no servidor.

```text
Motor V8 (o mesmo do Chrome) + APIs de sistema (arquivos, rede, processos)
```

Antes do Node: JS só rodava no browser. Depois do Node: a mesma linguagem faz frontend **e** backend.

## Por que Node.js é popular

- **Uma linguagem só** — quem sabe JS já programa backend
- **I/O não-bloqueante** — lida com milhares de conexões simultâneas sem criar uma thread por conexão
- **npm** — o maior repositório de pacotes do mundo
- **Ecossistema** — Express, Fastify, NestJS, Prisma...

## O modelo de I/O não-bloqueante

Node usa uma única thread com **event loop** — operações lentas (leitura de disco, HTTP, banco) são delegadas e o código continua:

```javascript
// Não para o servidor esperando o arquivo — registra um callback
const fs = require("fs");

fs.readFile("dados.txt", "utf8", (erro, dados) => {
  console.log(dados); // executa quando o arquivo terminar de ler
});

console.log("Isso roda PRIMEIRO, sem esperar");
```

## O que Node NÃO é

- Não é uma linguagem (a linguagem é JavaScript/TypeScript)
- Não é um framework (Express é o framework; Node é o runtime)
- Não é bom para CPU pesada (processamento de imagem, criptografia intensiva — para isso há worker threads ou outras linguagens)

## Onde Node brilha

- APIs REST e GraphQL
- Aplicações em tempo real (chat, websockets)
- CLIs e ferramentas de build
- Microsserviços
- SSR (Next.js roda em Node)

## Verificando a instalação

```bash
node --version   # v20.x.x
npm --version    # 10.x.x
```

## Resumo

- Backend = servidor: regras, dados e segurança
- Node.js = motor V8 + APIs de sistema → JS fora do browser
- Event loop + I/O não-bloqueante = muitas conexões numa thread
- Frameworks (Express) rodam em cima do Node
