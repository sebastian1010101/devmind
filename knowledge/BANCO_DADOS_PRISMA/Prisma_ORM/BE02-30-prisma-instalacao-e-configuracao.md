# BE02-30 — Prisma: Instalação e Configuração

## Setup em projeto Node/TS existente

```bash
npm install prisma --save-dev     # CLI (dev)
npm install @prisma/client        # Client (runtime)
npx prisma init                   # cria prisma/schema.prisma e .env
```

```text
projeto/
├─ prisma/
│  └─ schema.prisma     ← modelos
├─ .env                 ← DATABASE_URL
└─ package.json
```

`prisma` (CLI) vai em devDependencies — o `client` em dependencies.

## O schema inicial

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

- `generator` — gera o Client em JS/TS
- `datasource` — qual banco e de onde vem a URL
- `env("DATABASE_URL")` — lê do `.env` — a URL **não** fica no código

## DATABASE_URL

```env
DATABASE_URL="postgresql://usuario:senha@localhost:5432/meu_banco?schema=public"
```

```text
postgresql://  usuario  :  senha  @  host  :5432 / banco  ?schema=public
    │            │         │         │       │      │          │
 protocolo   usuário    senha    servidor  porta  database   schema do pg
```

Caracteres especiais na senha precisam de URL-encode (`@` → `%40`).

## Primeira model + migrate

```prisma
model Usuario {
  id    Int    @id @default(autoincrement())
  nome  String
  email String @unique
}
```

```bash
npx prisma migrate dev --name create_usuarios
```

Esse comando faz **três** coisas:

```text
1. cria prisma/migrations/<timestamp>_create_usuarios/migration.sql
2. aplica o SQL no banco (CREATE TABLE usuarios...)
3. regenera o Prisma Client
```

## Usando o Client

```ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const usuario = await prisma.usuario.create({
  data: { nome: "Ana", email: "ana@mail.com" },
});
```

Repare: `prisma.usuario` — o model `Usuario` vira propriedade **em camelCase minúsculo**.

## Comandos essenciais

| Comando | Faz |
| --- | --- |
| `npx prisma init` | Cria schema.prisma + .env |
| `npx prisma migrate dev --name x` | Migration + aplica + gera client |
| `npx prisma generate` | Só regenera o client |
| `npx prisma migrate deploy` | Aplica migrations pendentes (produção) |
| `npx prisma studio` | GUI no navegador para ver/editar dados |
| `npx prisma db push` | Empurra schema sem migration (prototipar) |

## Prisma Studio

```bash
npx prisma studio
```

Abre `localhost:5555` com tabelas navegáveis — ótimo para conferir dados sem SQL.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `Environment variable not found: DATABASE_URL` | `.env` na raiz, sem espaços, formato correto |
| `Can't reach database server` | Postgres rodando? host/porta certos? |
| `P1001` / authentication failed | Senha com caractere especial → URL-encode |
| Tipos desatualizados | Rode `npx prisma generate` |
| `.env` no git | `.env` no `.gitignore` — senha é segredo |

## Resumo

- `npm i -D prisma` + `npm i @prisma/client` + `npx prisma init`
- `DATABASE_URL` no `.env` — nunca no código nem no git
- `migrate dev --name x` = migration SQL + aplica + regenera Client
- `prisma studio` para inspecionar dados visualmente
