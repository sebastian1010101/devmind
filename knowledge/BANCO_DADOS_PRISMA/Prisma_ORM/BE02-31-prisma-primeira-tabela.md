# BE02-31 — Prisma: Primeira Tabela

## O model

No `schema.prisma`, um `model` declara uma tabela:

```prisma
model Usuario {
  id        Int      @id @default(autoincrement())
  nome      String
  email     String   @unique
  ativo     Boolean  @default(true)
  criadoEm  DateTime @default(now()) @map("criado_em")
}
```

## Anatomia do campo

```text
nomeDoCampo  Tipo  @atributos
─────────────────────────────
id           Int   @id @default(autoincrement())
email        String @unique
telefone     String?            ← ? = opcional (NULL)
```

## Tipos do schema → PostgreSQL

| Prisma | Postgres | Uso |
| --- | --- | --- |
| `Int` | integer | Ids, quantidades |
| `BigInt` | bigint | Números gigantes |
| `String` | text/varchar | Textos |
| `Boolean` | boolean | Flags |
| `DateTime` | timestamp | Datas e horários |
| `Float` | double precision | Flutuantes (evite p/ dinheiro) |
| `Decimal` | numeric | Dinheiro — exato |
| `Json` | jsonb | Dados semi-estruturados |

## Atributos comuns

| Atributo | Efeito |
| --- | --- |
| `@id` | Chave primária |
| `@unique` | Constraint unique |
| `@default(x)` | Valor padrão — `autoincrement()`, `now()`, `uuid()`, literal |
| `@map("col")` | Nome real da coluna no banco |
| `@@map("tabela")` | Nome real da tabela |
| `@@unique([a, b])` | Unique composta |
| `?` no tipo | Nullable |

```prisma
model Usuario {
  id    Int    @id @default(autoincrement())
  nome  String @map("nome_completo")

  @@map("usuarios")
}
```

Convenção: model em `PascalCase` no Prisma, tabela `snake_case` no banco via `@@map`.

## Migrate — levando pro banco

```bash
npx prisma migrate dev --name create_usuarios
```

```text
prisma/migrations/
└─ 20260927120000_create_usuarios/
   └─ migration.sql      ← o CREATE TABLE gerado
```

O SQL gerado é SQL normal — você pode (e deve) ler para entender o que mudou.

## Evoluindo a tabela

Adicionou campo? Edite o schema e migre de novo:

```prisma
model Usuario {
  // ...campos anteriores
  telefone String?    // novo campo opcional
}
```

```bash
npx prisma migrate dev --name add_telefone_usuario
```

Cada mudança = uma migration nova. O histórico fica versionado em `migrations/`.

## Campo obrigatório em tabela com dados

```prisma
telefone String   // NOT NULL em tabela populada → erro
```

O Postgres não consegue dar valor às linhas existentes. Opções:

1. `String?` — opcional, depois preencha
1. `@default("")` — valor padrão para as existentes
1. Migration manual preenchendo antes

## Checando no banco

```bash
npx prisma studio          # GUI
# ou no psql:
\d usuarios                -- confere a estrutura criada
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `Tabela` criada com nome estranho | `@@map("usuarios")` controla o nome |
| Campo NOT NULL em tabela populada falha | Adicione como `?` ou com `@default` |
| Editou o banco direto | Drift — o schema deve ser a fonte; use migrations |
| Renomear virou drop+create | Prisma pode interpretar renomear como delete+add — confira o SQL gerado |
| Migrations com conflito | `migrate dev` detecta drift — resolva com `migrate reset` em dev |

## Resumo

- `model` declara a tabela; campo = `nome Tipo @atributos`
- `@id`, `@unique`, `@default`, `?` cobrem o essencial
- `@@map`/`@map` separam nomes do código (camelCase) do banco (snake_case)
- Cada mudança de schema = `migrate dev --name` = nova migration versionada
