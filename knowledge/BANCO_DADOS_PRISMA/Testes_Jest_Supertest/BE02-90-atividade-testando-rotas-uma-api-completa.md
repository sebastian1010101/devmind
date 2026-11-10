# BE02-90 — Atividade: Testando Rotas de uma API Completa

## Objetivo

Suite de integração final — cobrindo a API de vagas/candidaturas inteira: auth, regras de negócio, autorização e erros.

## Escopo

```text
Auth:       POST /auth/register, POST /auth/login
Vagas:      GET (público), POST (auth), GET /:id (com candidaturas)
Candidaturas: POST /vagas/:id/candidaturas (auth)
              GET /minhas-candidaturas (auth)
              PATCH /candidaturas/:id (dono da vaga)
```

## Setup da suite

```ts
describe("Vagas API", () => {
  let candidatoToken: string;
  let candidatoId: number;
  let empresaToken: string;
  let empresaId: number;

  beforeEach(async () => {
    await prisma.candidatura.deleteMany();
    await prisma.vaga.deleteMany();
    await prisma.usuario.deleteMany();

    const [cand, empresa] = await Promise.all([
      prisma.usuario.create({ data: fixtureCandidato }),
      prisma.usuario.create({ data: fixtureEmpresa }),
    ]);
    candidatoId = cand.id;
    empresaId = empresa.id;
    candidatoToken = signToken(cand.id);
    empresaToken = signToken(empresa.id);
  });
});
```

## Casos-chave

```ts
it("fluxo completo: register → login → candidatar", async () => {
  // register
  const reg = await request(app).post("/auth/register").send({
    nome: "Nova", email: "nova@m.com", senha: "12345678",
  });
  expect(reg.status).toBe(201);

  // login
  const login = await request(app).post("/auth/login").send({
    email: "nova@m.com", senha: "12345678",
  });
  expect(login.body).toHaveProperty("accessToken");

  // candidatar com o token novo
  const vaga = await criarVaga({ empresaId });
  const cand = await request(app)
    .post(`/vagas/${vaga.id}/candidaturas`)
    .set("Authorization", `Bearer ${login.body.accessToken}`);

  expect(cand.status).toBe(201);
});

it("candidatura dupla → 409", async () => {
  const vaga = await criarVaga({ empresaId });

  await request(app)
    .post(`/vagas/${vaga.id}/candidaturas`)
    .set("Authorization", `Bearer ${candidatoToken}`);

  const res = await request(app)
    .post(`/vagas/${vaga.id}/candidaturas`)
    .set("Authorization", `Bearer ${candidatoToken}`);

  expect(res.status).toBe(409);
});

it("PATCH /candidaturas/:id — só dono da vaga muda status", async () => {
  const candidatura = await criarCandidatura(vaga.id, candidatoId);

  // candidato tenta mudar — não é dele
  const resCand = await request(app)
    .patch(`/candidaturas/${candidatura.id}`)
    .set("Authorization", `Bearer ${candidatoToken}`)
    .send({ status: "aprovada" });
  expect(resCand.status).toBe(403);

  // dono da vaga muda
  const resEmp = await request(app)
    .patch(`/candidaturas/${candidatura.id}`)
    .set("Authorization", `Bearer ${empresaToken}`)
    .send({ status: "entrevista" });
  expect(resEmp.status).toBe(200);
});

it("GET /minhas-candidaturas — só as minhas", async () => {
  const outro = await criarCandidato();
  await criarCandidatura(vaga1.id, candidatoId);
  await criarCandidatura(vaga2.id, outro.id);   // de outro

  const res = await request(app)
    .get("/minhas-candidaturas")
    .set("Authorization", `Bearer ${candidatoToken}`);

  expect(res.body).toHaveLength(1);
  expect(res.body[0].candidatoId).toBe(candidatoId);
});
```

## Matriz de cobertura

| Rota | Casos |
| --- | --- |
| register | 201, 409 email, 400 body |
| login | 200 token, 401 senha errada, 401 email inexistente |
| vagas POST | 201 auth, 401 sem token, 400 dados |
| candidaturas POST | 201, 409 dupla, 404 vaga, 401 sem token |
| candidaturas PATCH | 200 dono, 403 não-dono, 404 inexistente |
| minhas | 200 só as próprias, 401 sem token |

## Critérios de conclusão

1. Fluxo end-to-end (register→login→ação) passando
1. Autorização por papel testada (403 do candidato)
1. Filtro "minhas" realmente filtrando (id de outro não vaza)
1. `beforeEach` com fixtures controladas

## Resumo

- Suite completa = auth + regra de negócio + autorização + bordas
- Fixtures no `beforeEach` criam os atores do cenário
- 403 de "não é seu" é o teste mais valioso de autorização
- Asserts semânticos em cada caminho — sucesso e erro
