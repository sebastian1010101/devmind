# BE02-29 — Introdução ao ORM Prisma

## O que é um ORM

**ORM** (Object-Relational Mapper) é a ponte entre o mundo dos objetos (sua aplicação) e o mundo das tabelas (o banco):

```text
Sem ORM:                            Com ORM:
─────────                           ─────────
código → SQL → resultado          código → objetos → resultado
         parsear linhas                    ↑
         montar objetos              o ORM faz isso
```

```ts
// sem ORM — SQL manual
const res = await pool.query(
  "INSERT INTO usuarios (nome, email) VALUES ($1, $2) RETURNING *",
  [nome, email]
);
const usuario = res.rows[0];

// com Prisma — mesma operação
const usuario = await prisma.usuario.create({
  data: { nome, email }
});
```

## Por que usar

| SQL manual | ORM (Prisma) |
| --- | --- |
| Strings de SQL — erro só em runtime | API tipada — erro em tempo de compilação |
| Resultado é `any`/`rows[]` | Resultado tipado automaticamente |
| Migrations manuais | `migrate` versiona o schema |
| JOINs manuais | `include` carrega relações |
| SQL injection se desleixar | Queries parametrizadas por padrão |

## O que é o Prisma

ORM moderno para Node/TypeScript com 3 peças:

```text
schema.prisma  →  você descreve os modelos
      │
      ├── prisma migrate  → gera e aplica SQL no banco
      └── prisma generate → gera o Prisma Client tipado
```

| Peça | Papel |
| --- | --- |
| **Schema** (`schema.prisma`) | Declara models, campos, tipos e relações |
| **Migrate** | Transforma o schema em SQL versionado |
| **Client** (`@prisma/client`) | API TypeScript gerada a partir do schema |

## O schema — exemplo

```prisma
model Usuario {
  id        Int      @id @default(autoincrement())
  nome      String
  email     String   @unique
  criadoEm  DateTime @default(now())
}
```

O modelo declarativo vira tabela no Postgres — o Prisma escreve o `CREATE TABLE` por você.

## O fluxo de trabalho

```text
1. edita schema.prisma
2. npx prisma migrate dev --name descricao
   ├─ gera migration SQL (versionada em prisma/migrations/)
   ├─ aplica no banco
   └─ regenera o Client
3. usa prisma.usuario.create() no código — já tipado
```

## Type safety — o grande diferencial

```ts
const u = await prisma.usuario.findUnique({ where: { email } });
//    ↑ tipado: Usuario | null — autocomplete e erro em compile

u.nome       // ✅ existe
u.telefone   // ❌ erro de compilação — campo não existe no model
```

O Client é **gerado do seu schema** — mude o schema, o tipo muda junto.

## Quando o SQL ainda aparece

- Queries muito específicas: `prisma.$queryRaw` permite SQL cru
- O Prisma mostra o SQL gerado com `log: ["query"]` — bom para aprender

## Erros comuns

| Erro | Correção |
| --- | --- |
| Editou schema mas Client desatualizado | `migrate dev` ou `prisma generate` |
| Esperar que Prisma "adivinhe" o banco | O schema é a fonte da verdade — edite-o primeiro |
| `any` nos resultados | `@prisma/client` não foi gerado — rode `generate` |
| Achar que ORM elimina precisar saber SQL | ORM abstrai, não elimina — SQL continua valendo |

## Resumo

- ORM mapeia tabelas↔objetos: escreve código, não strings de SQL
- Prisma = `schema.prisma` (declarativo) + `migrate` (versiona) + `Client` (tipado)
- Resultado tipado do schema — autocomplete e erros em compile time
- Queries parametrizadas por padrão — SQL injection eliminado por design
