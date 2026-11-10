# BE02-97 — Passo a Passo: Testando API de To Do

## A aula de consolidação

Aplica o stack inteiro de testes numa API de tarefas — unitários no service, integração nas rotas.

## A API

```prisma
model Tarefa {
  id         Int      @id @default(autoincrement())
  titulo     String
  concluida  Boolean  @default(false)
  criadoEm   DateTime @default(now()) @map("criado_em")

  @@map("tarefas")
}
```

```text
POST   /tarefas        → cria
GET    /tarefas        → lista (filtro ?concluida=)
GET    /tarefas/:id    → detalhe
PATCH  /tarefas/:id    → concluir/renomear
DELETE /tarefas/:id    → remove
```

## Camada unitária — service com mock

```ts
const prismaMock = mockDeep<PrismaClient>();
const service = new TarefaService(prismaMock as unknown as PrismaClient);

describe("TarefaService", () => {
  beforeEach(() => mockReset(prismaMock));

  it("cria com concluida=false default", async () => {
    prismaMock.tarefa.create.mockResolvedValue({ id: 1, concluida: false } as any);
    const t = await service.criar({ titulo: "Estudar" });
    expect(t.concluida).toBe(false);
  });

  it("concluir lança 404 quando não existe", async () => {
    prismaMock.tarefa.findUnique.mockResolvedValue(null);
    await expect(service.concluir(9)).rejects.toMatchObject({ statusCode: 404 });
  });

  it("concluir não reconclui a já concluída", async () => {
    prismaMock.tarefa.findUnique.mockResolvedValue({ id: 1, concluida: true } as any);
    await expect(service.concluir(1)).rejects.toThrow();
    expect(prismaMock.tarefa.update).not.toHaveBeenCalled();
  });
});
```

## Camada de integração — rotas com banco

```ts
describe("Tarefas API", () => {
  beforeAll(() => prisma.$connect());
  beforeEach(() => prisma.tarefa.deleteMany());
  afterAll(() => prisma.$disconnect());

  it("fluxo: cria → lista → conclui → delete", async () => {
    const criada = await request(app).post("/tarefas").send({ titulo: "X" });
    expect(criada.status).toBe(201);
    expect(criada.body.concluida).toBe(false);

    const lista = await request(app).get("/tarefas");
    expect(lista.body).toHaveLength(1);

    const concluida = await request(app)
      .patch(`/tarefas/${criada.body.id}`)
      .send({ concluida: true });
    expect(concluida.body.concluida).toBe(true);

    const del = await request(app).delete(`/tarefas/${criada.body.id}`);
    expect(del.status).toBe(204);

    const vazia = await request(app).get("/tarefas");
    expect(vazia.body).toHaveLength(0);
  });

  it("PATCH inexistente → 404", async () => {
    const res = await request(app).patch("/tarefas/999").send({ concluida: true });
    expect(res.status).toBe(404);
  });

  it("POST sem titulo → 400", async () => {
    const res = await request(app).post("/tarefas").send({});
    expect(res.status).toBe(400);
  });

  it("filtro ?concluida=true", async () => {
    await prisma.tarefa.create({ data: { titulo: "A", concluida: true } });
    await prisma.tarefa.create({ data: { titulo: "B" } });

    const res = await request(app).get("/tarefas?concluida=true");
    expect(res.body).toHaveLength(1);
    expect(res.body[0].titulo).toBe("A");
  });
});
```

## O que a passo a passo consolida

```text
unitário:    regra "não reconclui" provada sem banco
integração:  CRUD inteiro contra Postgres de teste
             default, filtro, 404/400 semânticos
```

## Ordem sugerida de implementação

1. Service + unitários (mock) — regras isoladas
1. Rotas + integração — HTTP + banco
1. Validação (Zod) + casos de 400
1. Filtros/edge cases

## Resumo

- To-do é o CRUD canônico — ótimo para consolidar o fluxo inteiro
- Unitários cobrem a regra; integração cobre a rota+banco
- `?concluida=` prova que query param filtra de verdade
- Suite verde = registro/edição/exclusão/filtro todos provados
