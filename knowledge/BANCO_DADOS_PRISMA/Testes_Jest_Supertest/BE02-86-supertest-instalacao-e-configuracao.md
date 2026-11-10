# BE02-86 — Supertest: Instalação e Configuração

## O que é

**Supertest** faz requisições HTTP ao seu app Express **sem subir servidor** — teste de integração da camada HTTP.

```text
request(app).post("/usuarios").send({...})
        ↓
Express app → rotas → middlewares → service → resposta
        ↓
expect(res.status).toBe(201)
```

## Setup

```bash
npm install -D supertest @types/supertest
```

## O app separado do server

A divisão clássica — `app` exportável, `server` só escuta:

```ts
// src/app.ts — o app sem listen
import express from "express";
export const app = express();
app.use(express.json());
app.use("/usuarios", usuarioRouter);
```

```ts
// src/server.ts — só sobe
import { app } from "./app";
app.listen(process.env.PORT || 3000);
```

```ts
// teste — usa app, nunca server
import request from "supertest";
import { app } from "../src/app";

const res = await request(app).get("/usuarios");
```

**Regra**: teste usa `app`; produção usa `server`. Se o teste sobe porta, trava e conflita.

## O primeiro request

```ts
describe("GET /usuarios", () => {
  it("retorna 200 e lista", async () => {
    const res = await request(app).get("/usuarios");

    expect(res.status).toBe(200);
    expect(res.body).toBeInstanceOf(Array);
  });
});
```

## A API encadeada

```ts
await request(app)
  .post("/usuarios")
  .send({ nome: "Ana", email: "a@a.com" })    // body JSON
  .set("Authorization", `Bearer ${token}`)    // header
  .expect(201);                                // assert inline de status

// ou pegar a resposta e assertar
const res = await request(app).post("/login").send(creds);
expect(res.status).toBe(200);
expect(res.body).toHaveProperty("accessToken");
```

## Com banco de teste

```json
"test": "dotenv -e .env.test -- jest --runInBand"
```

```env
# .env.test
DATABASE_URL="postgresql://postgres:senha@localhost:5432/api_test"
```

```ts
beforeAll(async () => {
  await prisma.$connect();
});

beforeEach(async () => {
  await prisma.usuario.deleteMany();   // banco limpo por teste
});

afterAll(async () => {
  await prisma.$disconnect();
});
```

## Asserts úteis

```ts
expect(res.status).toBe(201);
expect(res.body.email).toBe("a@a.com");
expect(res.body).toHaveProperty("id");
expect(res.body).not.toHaveProperty("senha");   // hash nunca vaza
expect(res.headers["content-type"]).toMatch(/json/);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `app.listen` no teste | Exporte `app`; `server.ts` separado escuta |
| Testes concorrendo no banco | `--runInBand` + `.env.test` dedicado |
| `Cannot POST` | Falta `express.json()` ou rota errada |
| Timeout / hanging | `afterAll` sem `$disconnect` — conexão aberta |
| 401 inesperado | `.set("Authorization", "Bearer " + token)` |

## Resumo

- Supertest testa HTTP **sem porta** — `request(app)`
- `app` exportável; `server.ts` só faz listen
- `.send()` body, `.set()` headers, `.expect()` status
- `.env.test` + `deleteMany` em `beforeEach` — banco isolado por teste
