# BE02-60 — Dotenv

## O que é

Biblioteca que carrega variáveis de ambiente de um arquivo `.env` para `process.env`:

```bash
npm install dotenv
```

## O `.env`

```bash
# .env — NUNCA commite
DATABASE_URL="postgres://user:pass@localhost:5432/meudb"
JWT_SECRET="segredo-super-forte"
PORT=3000
NODE_ENV=development
```

## Carregando

```typescript
// No topo do entry point — ANTES de tudo que usa env
import "dotenv/config";

// ou explicitamente
import dotenv from "dotenv";
dotenv.config();

process.env.DATABASE_URL; // "postgres://..."
process.env.PORT;         // "3000" — sempre string!
```

## Regra de ouro — antes de tudo

```typescript
// ❌ errado — prisma lê DATABASE_URL antes do dotenv carregar
import { prisma } from "./database/prisma";
import "dotenv/config";

// ✅ certo — dotenv primeiro
import "dotenv/config";
import { prisma } from "./database/prisma";
```

`import "dotenv/config"` no topo garante que `process.env` está populado antes dos outros módulos executarem.

## `.env` no `.gitignore` — obrigatório

```text
# .gitignore
node_modules/
dist/
.env
.env.local
```

Segredos no git = vazamento. Quem clona cria seu próprio `.env`.

## `.env.example` — o compromisso

```bash
# .env.example — commitado, sem valores reais
DATABASE_URL="postgres://user:pass@localhost:5432/db_name"
JWT_SECRET="your-secret-here"
PORT=3000
```

Documenta quais vars existem sem expor valores — quem clona sabe o que configurar.

## `process.env` é string — sempre

```typescript
const porta = process.env.PORT;           // "3000" — string
const porta = Number(process.env.PORT);   // 3000 — converta
const porta = parseInt(process.env.PORT ?? "3000", 10);
```

## Validando env no boot

```typescript
const obrigatorias = ["DATABASE_URL", "JWT_SECRET"];
for (const v of obrigatorias) {
  if (!process.env[v]) {
    throw new Error(`Variável de ambiente faltando: ${v}`);
  }
}
```

Falha rápida no boot — melhor que crash misterioso no primeiro request.

## Resumo

- `.env` carrega vars locais; `dotenv/config` no topo do entry point
- `.env` no gitignore; `.env.example` commitado como documentação
- `process.env.X` sempre string — converta números
- Valide vars obrigatórias no boot — falhe rápido
