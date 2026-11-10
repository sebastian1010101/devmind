# BE02-88 — Atividade: Testando Rotas de uma API

## Objetivo

Escrever suite de integração cobrindo as rotas de uma API de produtos — CRUD completo, erros e autenticação.

## Rotas sob teste

```text
POST   /produtos       → cria (auth)
GET    /produtos       → lista (público)
GET    /produtos/:id   → detalhe
PATCH  /produtos/:id   → atualiza (auth, dono)
DELETE /produtos/:id   → remove (auth, dono)
POST   /login          → token
```

## Estrutura da suite

```ts
import request from "supertest";
import { app } from "../src/app";
import { prisma } from "../src/database/prisma";

describe("Produtos API", () => {
  let token: string;
  let usuarioId: number;

  beforeAll(async () => {
    await prisma.$connect();
  });

  beforeEach(async () => {
    await prisma.produto.deleteMany();
    await prisma.usuario.deleteMany();

    const usuario = await prisma.usuario.create({
      data: { nome: "Vendedor", email: "v@v.com", senha: await bcrypt.hash("12345678", 10) },
    });
    usuarioId = usuario.id;
    token = jwt.sign({}, process.env.JWT_SECRET!, { subject: String(usuario.id) });
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });
});
```

Use sempre o mesmo custo (`10`) de produção — reduzir para acelerar o teste é tentador, mas custo baixo demais não representa o comportamento real e é fácil copiar por acidente para código de produção. Se a suite ficar lenta pelo hash, mova a criação de usuários fixos para o `beforeAll` em vez de reduzir o custo.

## Os casos

```ts
it("POST /produtos — 201 autenticado", async () => {
  const res = await request(app)
    .post("/produtos")
    .set("Authorization", `Bearer ${token}`)
    .send({ nome: "Teclado", preco: 250 });

  expect(res.status).toBe(201);
  expect(res.body.usuarioId).toBe(usuarioId);   // dono veio do token
});

it("POST /produtos — 401 sem token", async () => {
  const res = await request(app)
    .post("/produtos")
    .send({ nome: "Teclado" });

  expect(res.status).toBe(401);
});

it("GET /produtos/:id — 404 inexistente", async () => {
  const res = await request(app).get("/produtos/9999");
  expect(res.status).toBe(404);
});

it("PATCH /produtos/:id — 403 de outro dono", async () => {
  const produto = await prisma.produto.create({
    data: { nome: "Mouse", preco: 100, usuarioId },
  });

  // token de OUTRO usuário
  const outroToken = jwt.sign({}, process.env.JWT_SECRET!, { subject: "999" });

  const res = await request(app)
    .patch(`/produtos/${produto.id}`)
    .set("Authorization", `Bearer ${outroToken}`)
    .send({ preco: 90 });

  expect(res.status).toBe(403);
});
```

## O que cada assert prova

| Assert | Garante |
| --- | --- |
| `201` | Criou — não `200` |
| `usuarioId = usuarioId` | Dono veio do token, não do body |
| `401` sem token | Middleware protegeu |
| `404` id inexistente | Tratamento de P2025/findUnique |
| `403` outro dono | Autorização por propriedade |

## Critérios de conclusão

1. Suite cobre create, read, update, delete + auth
1. `beforeEach` cria usuário e token frescos
1. Asserts semânticos (201/401/403/404, não só "erro")
1. Efeito no banco conferido quando importa

## Resumo

- Token no `beforeEach` — custo baixo de hash em teste
- 403 vs 404 vs 401 — status semântico importa no assert
- `res.body` valida shape; `prisma.` confirma o banco
