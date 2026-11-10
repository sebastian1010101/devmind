# BE02-40 — Prisma: Create Many

## O básico

```ts
const resultado = await prisma.usuario.createMany({
  data: [
    { nome: "Ana", email: "ana@mail.com" },
    { nome: "Bruno", email: "bruno@mail.com" },
    { nome: "Carla", email: "carla@mail.com" },
  ],
});
// resultado → { count: 3 }
```

Vira um `INSERT` com múltiplos `VALUES` — uma query só, muito mais rápido que N `create`s.

## A diferença do create

| `create` | `createMany` |
| --- | --- |
| 1 registro por chamada | N registros numa query |
| Retorna o objeto criado | Retorna `{ count: N }` |
| Aceita nested write (`create: {...}`) | **Não** aceita relações aninhadas |
| `select`/`include` disponíveis | Sem retorno dos dados |

## skipDuplicates

```ts
await prisma.usuario.createMany({
  data: [
    { nome: "Ana", email: "ana@mail.com" },
    { nome: "Ana", email: "ana@mail.com" },   // duplicata
  ],
  skipDuplicates: true,   // ignora em vez de estourar P2002
});
```

É o `ON CONFLICT DO NOTHING` do SQL — só funciona em Postgres/MySQL/SQLite.

## createManyAndReturn

Versões recentes do Prisma (5.14+) suportam retorno em Postgres:

```ts
const criados = await prisma.usuario.createManyAndReturn({
  data: [
    { nome: "Ana", email: "ana@mail.com" },
    { nome: "Bruno", email: "bruno@mail.com" },
  ],
});
// criados → Usuario[] com ids!
```

Resolve a maior limitação do `createMany` clássico.

## Quando usar

| Cenário | Ferramenta |
| --- | --- |
| Seed de dados | `createMany` — bulk rápido |
| Importação/CSV | `createMany` em lotes de ~1000 |
| Precisa dos ids de volta | `createManyAndReturn` (pg) ou creates em `$transaction` |
| Precisa criar relações junto | `create` com nested — `createMany` não faz |

## Seeds realistas

```ts
// prisma/seed.ts
const usuarios = Array.from({ length: 100 }, (_, i) => ({
  nome: `Usuario ${i}`,
  email: `user${i}@mail.com`,
}));

await prisma.usuario.createMany({ data: usuarios });
```

```json
// package.json
"prisma": { "seed": "ts-node prisma/seed.ts" }
```

```bash
npx prisma db seed
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Precisar dos ids criados | `createMany` não retorna — use `createManyAndReturn` ou `create` |
| Nested create dentro de createMany | Não suportado — crie pais e filhos separadamente |
| P2002 no meio do lote | `skipDuplicates: true` ou dedupe os dados antes |
| Lote gigante estourando | Quebre em chunks de 500–1000 |

## Resumo

- `createMany` = um INSERT de N linhas — retorna `{ count }`
- Sem nested relations, sem retorno dos objetos (a menos que `createManyAndReturn`)
- `skipDuplicates: true` = `ON CONFLICT DO NOTHING`
- Ideal para seeds e importações em massa
