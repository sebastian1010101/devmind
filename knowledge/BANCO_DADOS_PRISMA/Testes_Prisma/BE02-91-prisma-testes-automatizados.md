# BE02-91 — Prisma: Testes Automatizados

## As duas estratégias

```text
Unitário:   service → PrismaClient MOCKADO    (sem banco)
Integração: service → PrismaClient real → banco de TESTE
```

| | Mock | Banco de teste |
| --- | --- | --- |
| Velocidade | ms | mais lento |
| O que prova | A lógica do service | Constraints, queries, FKs reais |
| Fragilidade | Mock pode divergir do Prisma real | Precisa de banco limpo |
| Cobertura | Regras de negócio | Contratos do banco |

As duas coexistem — unitários rápidos pra lógica, integração pra queries.

## Por que testar a camada Prisma

- `@unique`/`@relation`/FKs são comportamento — mock não prova que `P2002` acontece
- `include`, `where` com `some`/`none` — a query real pode divergir do esperado
- Migrations e o código precisam concordar

## O banco de teste

```env
# .env.test
DATABASE_URL="postgresql://postgres:senha@localhost:5432/api_test"
```

```bash
npx dotenv -e .env.test -- npx prisma migrate deploy   # sobe o schema no banco de teste
```

```json
"test": "dotenv -e .env.test -- jest --runInBand"
```

```text
api_dev    → npm run dev
api_test   → npm test       (banco separado!)
```

## O ciclo de vida dos testes

```ts
beforeAll(async () => {
  await prisma.$connect();
  // schema já aplicado pelo migrate deploy
});

beforeEach(async () => {
  // limpa as tabelas — isolamento por teste
  await prisma.candidatura.deleteMany();
  await prisma.vaga.deleteMany();
  await prisma.usuario.deleteMany();
});

afterAll(async () => {
  await prisma.$disconnect();
});
```

**Ordem do deleteMany importa** — filhos primeiro (FK).

## `--runInBand` — serialização

```bash
jest --runInBand
```

Suites paralelas no mesmo banco pisam uma na outra — `deleteMany` de uma suja o `create` da outra. Serial é o default sensato com banco compartilhado.

Alternativa mais robusta: **um schema/database por worker** ou transações rollback — avançado.

## O que muda do unitário

```ts
// unitário: o mock mente que tudo funciona
repoMock.criar.mockResolvedValue({ id: 1 });

// integração: o banco decide
await prisma.usuario.create({ data: { email: "dup@x.com" } });
await prisma.usuario.create({ data: { email: "dup@x.com" } });
// P2002 real — prova que a constraint existe
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Teste destruindo banco dev | `.env.test` separado — sempre |
| Suites em paralelo brigando | `--runInBand` ou banco por worker |
| `deleteMany` na ordem errada | Filhos antes dos pais (FK) |
| Migration do teste desatualizada | `migrate deploy` com `.env.test` antes de rodar |

## Resumo

- Mock prova lógica; banco de teste prova constraints e queries
- `.env.test` + `migrate deploy` + `deleteMany` no `beforeEach`
- `--runInBand` evita race entre suites no mesmo banco
- P2002/FK só existe de verdade contra banco real
