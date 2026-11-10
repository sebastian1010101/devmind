# BE02-95 — Prisma: Testes de Integração

## O que muda

```text
Unitário:   prismaMock → prova que o service CHAMA certo
Integração: prisma real → prova que o banco EXECUTA certo
```

Constraints, FKs, `@unique`, cascades — só existem no banco real.

## Setup — banco de teste dedicado

```env
# .env.test
DATABASE_URL="postgresql://postgres:senha@localhost:5432/api_test"
```

```bash
# aplica o schema no banco de teste uma vez
npx dotenv -e .env.test -- npx prisma migrate deploy
```

```json
"test:integration": "dotenv -e .env.test -- jest --runInBand __tests__/integration"
```

## O ciclo de vida

```ts
import { prisma } from "../../src/database/prisma";

describe("UsuarioService (integração)", () => {
  const service = new UsuarioService(prisma);   // client real

  beforeAll(async () => {
    await prisma.$connect();
  });

  beforeEach(async () => {
    await prisma.pedido.deleteMany();     // filhos primeiro
    await prisma.usuario.deleteMany();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });
});
```

## O que integração prova que mock não

```ts
it("@unique realmente barra duplicata", async () => {
  await service.criar({ email: "a@a.com", nome: "A", senha: "12345678" });

  await expect(service.criar({ email: "a@a.com", nome: "B", senha: "x" }))
    .rejects.toMatchObject({ statusCode: 409 });
});
```

O `P2002` saiu do Postgres — a constraint existe de verdade.

```ts
it("cascade deleta filhos junto", async () => {
  const autor = await prisma.autor.create({
    data: { nome: "X", livros: { create: [{ titulo: "T" }] } },
  });

  await prisma.autor.delete({ where: { id: autor.id } });

  const livros = await prisma.livro.findMany({ where: { autorId: autor.id } });
  expect(livros).toHaveLength(0);   // onDelete: Cascade provado
});
```

```ts
it("FK inválida lança", async () => {
  await expect(
    prisma.livro.create({ data: { titulo: "X", autorId: 999 } })
  ).rejects.toMatchObject({ code: "P2003" });
});
```

## Queries complexas — onde integração brilha

```ts
it("busca inclui relações aninhadas", async () => {
  await prisma.autor.create({
    data: { nome: "Machado", livros: { create: [{ titulo: "Casmurro" }] } },
  });

  const autor = await service.buscarComLivros(1);

  expect(autor.livros).toHaveLength(1);
  expect(autor.livros[0].titulo).toBe("Casmurro");
});
```

`include`, `where` com `some`/`none`, `orderBy` por relação — bugs de query só aparecem com banco real.

## Limpeza por transação — alternativa

```ts
beforeEach(async () => {
  await prisma.$executeRaw`TRUNCATE usuarios, pedidos RESTART IDENTITY CASCADE`;
});
```

`TRUNCATE CASCADE` limpa tudo e reseta sequences — mais rápido que N `deleteMany` em esquemas grandes.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `deleteMany` erra ordem | Filhos primeiro; ou `TRUNCATE ... CASCADE` |
| Schema do teste desatualizado | `migrate deploy` com `.env.test` antes da suite |
| Testes em paralelo conflitam | `--runInBand` |
| Fixture com dado residual | Limpe tudo no `beforeEach` — não confie no afterEach |

## Resumo

- Integração = service + client real + banco de teste dedicado
- Prova constraints, cascades, includes, filtros de relação
- `deleteMany`/`TRUNCATE` no `beforeEach`; serialização com `--runInBand`
- Complementa o unitário — um prova a chamada, o outro a execução
