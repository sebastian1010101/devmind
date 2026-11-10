# BE02-32 — Atividade: Banco de Dados com Prisma

## Objetivo

Do zero ao banco rodando: instalar o Prisma, configurar `DATABASE_URL`, declarar models, migrar e inserir/ler dados pelo Client.

## Checklist

```text
1. npm i -D prisma && npm i @prisma/client
2. npx prisma init
3. DATABASE_URL no .env
4. models no schema.prisma
5. npx prisma migrate dev --name init
6. script de teste com create/findMany
```

## Models sugeridos — biblioteca

```prisma
model Autor {
  id     Int     @id @default(autoincrement())
  nome   String
  pais   String?
  livros Livro[]

  @@map("autores")
}

model Livro {
  id             Int     @id @default(autoincrement())
  titulo         String
  anoPublicacao  Int     @map("ano_publicacao")
  autor          Autor   @relation(fields: [autorId], references: [id])
  autorId        Int     @map("autor_id")

  @@map("livros")
}
```

## Conexão

```env
DATABASE_URL="postgresql://postgres:senha@localhost:5432/biblioteca_prisma?schema=public"
```

```bash
npx prisma migrate dev --name init
```

## Script de teste

```ts
// src/test.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const autor = await prisma.autor.create({
    data: { nome: "Machado de Assis", pais: "Brasil" },
  });
  console.log("autor criado:", autor);

  await prisma.livro.create({
    data: {
      titulo: "Dom Casmurro",
      anoPublicacao: 1899,
      autorId: autor.id,
    },
  });

  const livros = await prisma.livro.findMany();
  console.log(livros);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
```

```bash
npx ts-node-dev src/test.ts
```

## Validando no Studio

```bash
npx prisma studio
```

Abra `autores` e `livros` — os registros criados pelo script devem aparecer.

## Critérios de conclusão

1. `migrate dev` rodou sem erros e `prisma/migrations/` existe
1. Tabelas visíveis no Studio/psql com nomes certos (`@@map`)
1. Script insere e lê dados — tipos do Client funcionando
1. `.env` fora do git

## Erros comuns

| Erro | Correção |
| --- | --- |
| `DATABASE_URL` não encontrada | `.env` na raiz do projeto, não em `src/` |
| `@prisma/client` sem tipos | `npm i @prisma/client` + `npx prisma generate` |
| `prisma.usuario` undefined | Model `Usuario` vira `prisma.usuario` — minúsculo |
| Conexão recusada | Postgres rodando? `psql -U postgres` funciona? |

## Resumo

- Fluxo completo: init → `.env` → models → `migrate dev` → Client
- Relação no Prisma usa `@relation` + campo FK — versão curta do 1-N
- `npx prisma studio` valida visualmente o que o script criou
