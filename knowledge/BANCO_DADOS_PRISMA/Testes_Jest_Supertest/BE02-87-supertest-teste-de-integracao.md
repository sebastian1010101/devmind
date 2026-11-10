# BE02-87 — Supertest: Teste de Integração

## O que integração testa

```text
HTTP → rota → middleware → service → Prisma → banco de teste → volta
```

Diferente do unitário (service isolado com mock), aqui **tudo roda de verdade** — exceto que o banco é o de teste.

## Testando o CRUD de usuários

```ts
import request from "supertest";
import { app } from "../src/app";
import { prisma } from "../src/database/prisma";

describe("Usuários API", () => {
  beforeAll(async () => {
    await prisma.$connect();
  });

  beforeEach(async () => {
    await prisma.usuario.deleteMany();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  it("POST /usuarios — cria com 201", async () => {
    const res = await request(app)
      .post("/usuarios")
      .send({ nome: "Ana", email: "ana@mail.com", senha: "12345678" });

    expect(res.status).toBe(201);
    expect(res.body).toHaveProperty("id");
    expect(res.body.email).toBe("ana@mail.com");
    expect(res.body).not.toHaveProperty("senha");
  });

  it("POST /usuarios — 409 em email duplicado", async () => {
    await request(app)
      .post("/usuarios")
      .send({ nome: "Ana", email: "ana@mail.com", senha: "12345678" });

    const res = await request(app)
      .post("/usuarios")
      .send({ nome: "Outra", email: "ana@mail.com", senha: "outra123" });

    expect(res.status).toBe(409);
  });

  it("GET /usuarios — lista", async () => {
    await prisma.usuario.create({
      data: { nome: "Bruno", email: "b@b.com", senha: "hash" },
    });

    const res = await request(app).get("/usuarios");

    expect(res.status).toBe(200);
    expect(res.body).toHaveLength(1);
  });
});
```

## O padrão: seed no teste

```ts
// seed direto via prisma — prepara o estado
await prisma.usuario.create({ data: { ... } });

// ou helper
async function criarUsuario(dados = {}) {
  return prisma.usuario.create({
    data: { nome: "Padrão", email: "p@p.com", senha: "x", ...dados },
  });
}
```

O teste monta seu próprio cenário — **não depende de outro teste**.

## Asserts que importam

```ts
// status semântico
expect(res.status).toBe(404);   // não "qualquer erro"
// shape da resposta
expect(res.body).toMatchObject({ id: 1, email: "a@a.com" });
// o banco também — efeito real conferido
const noBanco = await prisma.usuario.findUnique({ where: { id } });
expect(noBanco).not.toBeNull();
```

A resposta e o **banco** podem divergir — confira os dois quando faz sentido.

## Testando rotas protegidas

```ts
let token: string;

beforeEach(async () => {
  await prisma.usuario.deleteMany();
  const usuario = await criarUsuario();
  token = jwt.sign({}, SECRET, { subject: String(usuario.id) });
});

it("GET /me retorna o usuário", async () => {
  const res = await request(app)
    .get("/me")
    .set("Authorization", `Bearer ${token}`);

  expect(res.status).toBe(200);
  expect(res.body.email).toBe("p@p.com");
});

it("GET /me sem token → 401", async () => {
  const res = await request(app).get("/me");
  expect(res.status).toBe(401);
});
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Teste depende do anterior | `beforeEach` limpa e re-seeda |
| `res.body.senha` presente | Bug real — `select` na rota omite |
| Timeout aleatório | Conexão aberta — `afterAll $disconnect` |
| Testes paralelos brigam | `--runInBand` no mesmo banco |

## Resumo

- Integração = rota + middleware + service + banco de teste, de verdade
- `beforeEach` limpa e seeda — teste independente
- Asserte status semântico, shape do body e **efeito no banco**
- Rotas protegidas: gere token no `beforeEach` e mande no `.set`
