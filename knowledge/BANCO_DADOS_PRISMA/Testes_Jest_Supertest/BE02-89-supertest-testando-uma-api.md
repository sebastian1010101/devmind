# BE02-89 — Supertest: Testando uma API

## Indo além do CRUD

Aula de aprofundamento — cenários menos óbvios que a suite precisa cobrir.

## Validação de entrada (Zod/middleware)

```ts
it("POST /usuarios — 400 com body inválido", async () => {
  const res = await request(app)
    .post("/usuarios")
    .send({ nome: "Ana" });          // sem email/senha

  expect(res.status).toBe(400);
  expect(res.body).toHaveProperty("message");
  // se o middleware retorna issues do Zod:
  expect(res.body.errors).toBeDefined();
});
```

Todo middleware de validação merece um `400` no teste — sem testar, o `500` passa batido.

## Paginação

```ts
it("GET /usuarios — pagina", async () => {
  await prisma.usuario.createMany({
    data: Array.from({ length: 25 }, (_, i) => ({
      nome: `User ${i}`, email: `u${i}@m.com`, senha: "x",
    })),
  });

  const p1 = await request(app).get("/usuarios?page=1&pageSize=10");
  const p2 = await request(app).get("/usuarios?page=2&pageSize=10");

  expect(p1.body.data).toHaveLength(10);
  expect(p2.body.data).toHaveLength(10);
  expect(p1.body.meta.total).toBe(25);
});
```

## Relações — o include funciona?

```ts
it("GET /vagas/:id traz candidaturas", async () => {
  const vaga = await criarVaga();
  await criarCandidatura(vaga.id, candidato.id);

  const res = await request(app).get(`/vagas/${vaga.id}`);

  expect(res.body.candidaturas).toHaveLength(1);
  expect(res.body.candidaturas[0].candidato.nome).toBe("Ana");
});
```

O teste prova que o `include` aninhado chega na resposta — não só o status.

## Erro do middleware de auth — token adulterado

```ts
it("token adulterado → 401", async () => {
  const res = await request(app)
    .get("/me")
    .set("Authorization", `Bearer ${token}corrompido`);

  expect(res.status).toBe(401);
});

it("token expirado → 401", async () => {
  const expirado = jwt.sign({}, SECRET, { subject: "1", expiresIn: "0s" });
  await new Promise(r => setTimeout(r, 100));

  const res = await request(app).get("/me").set("Authorization", `Bearer ${expirado}`);
  expect(res.status).toBe(401);
});
```

## O que ainda vale testar

| Cenário | Por quê |
| --- | --- |
| Content-Type errado | `express.json()` rejeita → 400/415 |
| Query params (`?filtro=`) | Filtros são fonte de bug |
| Campos extras no body | API deve ignorar ou rejeitar — defina |
| `id` não numérico (`/abc`) | `Number("abc")` → NaN → comportamento? |

## O anti-padrão

```ts
// ❌ teste só de status
expect(res.status).toBe(200);

// ✅ status + shape + efeito
expect(res.status).toBe(200);
expect(res.body).toHaveLength(2);
const count = await prisma.usuario.count();
expect(count).toBe(2);
```

Status sem conteúdo prova pouco — a resposta pode estar vazia e passar.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Só testar 200/201 | Erros e bordas são o valor real |
| Não conferir o banco | A resposta pode mentir — confirme no Prisma |
| Ignorar paginação/relacionamento | `meta.total`, include aninhado — teste o shape |
| Suite gigante lenta | Seeds enxutos — crie só o que o teste usa |

## Resumo

- Além do CRUD: validação (400), paginação, relações, tokens ruins
- Status + shape + efeito no banco = assert completo
- Tokens adulterados/expirados merecem caso próprio
- Teste o que pode quebrar — não o que já funciona trivialmente
