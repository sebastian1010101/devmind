# BE02-38 — Prisma: Client

## O que é

`PrismaClient` é a classe gerada do seu schema — é por ela que todo acesso ao banco passa:

```ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
```

Cada `model` vira uma propriedade com os métodos CRUD:

```text
model Usuario → prisma.usuario
├─ .create()       .findUnique()    .update()
├─ .createMany()   .findFirst()     .updateMany()
├─ .upsert()       .findMany()      .delete()
│                  .count()         .deleteMany()
└─                                 .aggregate()
```

## Singleton — uma instância só

```ts
// ❌ um new por arquivo/rota → um pool por instância → conexões esgotadas
// ✅ instância única compartilhada

// src/database/prisma.ts
import { PrismaClient } from "@prisma/client";

export const prisma = new PrismaClient();
```

```ts
// nas rotas/services:
import { prisma } from "./database/prisma";
```

Com hot-reload (ts-node-dev, nodemon), o processo recria módulos — o padrão oficial de dev:

```ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

## Tudo é Promise

```ts
const usuario = await prisma.usuario.findUnique({ where: { id: 1 } });
```

```text
prisma.usuario.findUnique(...)
  → query gerada → enviada ao Postgres → Promise<Usuario | null>
```

Sempre `await` (ou `.then`) — sem isso você recebe a Promise, não o dado.

## Desconectando

```ts
await prisma.$disconnect();
```

Scripts pontuais desconectam no fim (`finally`) — servidores ficam conectados enquanto rodam.

## Log e debug

```ts
const prisma = new PrismaClient({ log: ["query", "error", "warn"] });
```

`log: ["query"]` imprime o SQL gerado — excelente para aprender o que o ORM traduz.

## Transações

```ts
// array sequencial — tudo ou nada
await prisma.$transaction([
  prisma.conta.update({ where: { id: 1 }, data: { saldo: { decrement: 100 } } }),
  prisma.conta.update({ where: { id: 2 }, data: { saldo: { increment: 100 } } }),
]);

// interativa — lógica entre as queries
await prisma.$transaction(async (tx) => {
  const conta = await tx.conta.findUnique({ where: { id: 1 } });
  if (conta.saldo < 100) throw new Error("saldo insuficiente");
  return tx.conta.update({ where: { id: 1 }, data: { saldo: { decrement: 100 } } });
});
```

`tx` é o client dentro da transação — se lançar erro, tudo é desfeito.

## Raw SQL — escape hatch

```ts
const usuarios = await prisma.$queryRaw`SELECT * FROM usuarios WHERE id = ${id}`;
await prisma.$executeRaw`TRUNCATE TABLE logs`;
```

Template string com `${}` = parametrizado (seguro). Nunca concatene string — `$queryRawUnsafe` abre porta para injection.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `Too many connections` | Vários `new PrismaClient()` — use singleton |
| Esquecer `await` | Recebe Promise — sempre `await` |
| `prisma.Usuario` com maiúscula | Models viram propriedades minúsculas: `prisma.usuario` |
| `P2025: record not found` | `update`/`delete`/`findUniqueOrThrow` em id inexistente |
| Processo não encerra | `$disconnect()` no finally do script |

## Resumo

- `PrismaClient` é gerado do schema — `prisma.<model>.<metodo>()`
- Uma instância por aplicação (singleton) — o pool é por instância
- Tudo retorna Promise; `$disconnect()` ao final de scripts
- `$transaction` para atomicidade; `$queryRaw` para SQL cru parametrizado
