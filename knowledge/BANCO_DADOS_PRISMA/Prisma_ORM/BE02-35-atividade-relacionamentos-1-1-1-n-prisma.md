# BE02-35 — Atividade: Relacionamentos 1-1 e 1-N com Prisma

## Objetivo

Reproduzir no Prisma o mesmo tipo de esquema da atividade SQL: um 1-1 e um 1-N convivendo — com migrations e consultas via Client.

## Modelo — plataforma de cursos (versão Prisma)

```prisma
model Instrutor {
  id     Int      @id @default(autoincrement())
  nome   String
  email  String   @unique
  bio    Bio?
  cursos Curso[]

  @@map("instrutores")
}

model Bio {
  id          Int       @id @default(autoincrement())
  resumo      String
  linkedin    String?
  instrutor   Instrutor @relation(fields: [instrutorId], references: [id])
  instrutorId Int       @unique @map("instrutor_id")

  @@map("bios")
}

model Curso {
  id          Int       @id @default(autoincrement())
  titulo      String
  instrutor   Instrutor @relation(fields: [instrutorId], references: [id])
  instrutorId Int       @map("instrutor_id")

  @@map("cursos")
}
```

Checklist do schema:

- `Bio.instrutorId` tem `@unique` → 1-1
- `Curso.instrutorId` sem `@unique` → 1-N
- `Instrutor` declara os dois lados: `bio Bio?` e `cursos Curso[]`

```bash
npx prisma migrate dev --name cursos_1_1_1_n
```

## Script de teste

```ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // 1-1 + 1-N num create só
  const paula = await prisma.instrutor.create({
    data: {
      nome: "Paula",
      email: "paula@mail.com",
      bio: { create: { resumo: "Dev há 10 anos" } },
      cursos: {
        create: [{ titulo: "SQL do Zero" }, { titulo: "React Avançado" }],
      },
    },
    include: { bio: true, cursos: true },
  });
  console.log(paula);

  // 1-N: instrutor com contagem de cursos
  const instrutores = await prisma.instrutor.findMany({
    include: { _count: { select: { cursos: true } } },
  });
  console.log(instrutores.map(i => [i.nome, i._count.cursos]));

  // 1-1: bio do instrutor
  const bio = await prisma.bio.findUnique({
    where: { instrutorId: paula.id },   // @unique permite findUnique por FK
    include: { instrutor: true },
  });
  console.log(bio);
}

main().finally(() => prisma.$disconnect());
```

## Validando as regras

```ts
// deve falhar: segunda bio para o mesmo instrutor
await prisma.bio.create({ data: { resumo: "outra", instrutorId: paula.id } });
// P2002: Unique constraint failed on the fields: (instrutor_id)

// deve falhar: curso com instrutor inexistente
await prisma.curso.create({ data: { titulo: "X", instrutorId: 99 } });
// P2003: Foreign key constraint failed
```

Erros `P2002` (unique) e `P2003` (FK) são as constraints do SQL agindo — o Prisma só repassa.

## Critérios de conclusão

1. Migration criada com UNIQUE na FK de `bios` e FK simples em `cursos`
1. Create aninhado com `bio` + `cursos` funcionando
1. `findUnique` por `instrutorId` na bio (só funciona por ser `@unique`)
1. P2002 e P2003 observados nos testes de violação

## Resumo

- Mesma lógica do SQL: `@unique` na FK = 1-1; FK simples = 1-N
- `include` com múltiplas relações funciona junto
- Erros do Prisma (`P2002`, `P2003`) espelham as constraints do banco
