# BE01-51 — Arquitetura: Server e App

## Por que separar

```typescript
// ❌ app.ts tudo junto — impossível importar sem subir porta
const app = express();
// ... rotas, middlewares
app.listen(3000);
```

```typescript
// ✅ app.ts — configura a aplicação, exporta
const app = express();
app.use(express.json());
app.use("/produtos", produtosRouter);
app.use(handleErrors);
export default app;
```

```typescript
// ✅ server.ts — só sobe o servidor
import app from "./app";

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 http://localhost:${PORT}`));
```

## O ganho principal: testes

```typescript
// Teste importa app SEM subir porta
import request from "supertest";
import app from "../src/app";

test("GET /produtos retorna 200", async () => {
  const res = await request(app).get("/produtos");
  expect(res.status).toBe(200);
});
```

`supertest(app)` precisa do app **sem** `listen` — separar torna a app testável.

## Responsabilidades divididas

| `app.ts` | `server.ts` |
| --- | --- |
| `express()` | `app.listen(porta)` |
| `express.json()` | ler `process.env.PORT` |
| routers montados | log de inicialização |
| middlewares globais | shutdown gracioso |
| error-handler | |

## Estrutura completa final

```text
src/
├── app.ts                  → composição: middlewares + routers + errors
├── server.ts               → entry point: listen
├── routes/                 → endpoints
├── controllers/            → HTTP ↔ service
├── services/               → regras de negócio
├── repositories/           → acesso a dados
├── interfaces/             → contratos e DTOs
├── middlewares/            → validação, auth, handleErrors
├── errors/                 → AppError e subclasses
└── database/               → array em memória / conexão
```

## server.ts com shutdown gracioso

```typescript
import app from "./app";

const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, () => {
  console.log(`Servidor na porta ${PORT}`);
});

// Encerra limpo ao receber SIGTERM (deploy, docker stop)
process.on("SIGTERM", () => {
  server.close(() => process.exit(0));
});
```

## Entry point no package.json

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js"
  }
}
```

O entry point é `server.ts` — nunca `app.ts`.

## Resumo

- `app.ts` compõe e exporta; `server.ts` sobe a porta
- Sem separação, testes não conseguem importar a app
- Scripts apontam para `server` — dev e produção
- `SIGTERM` handler = encerramento limpo em containers
