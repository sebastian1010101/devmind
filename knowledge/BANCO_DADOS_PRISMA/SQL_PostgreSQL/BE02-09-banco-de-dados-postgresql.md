# BE02-09 — Banco de Dados: PostgreSQL

## O que é

**PostgreSQL** (ou só "Postgres") é um SGBD relacional open source, ativo desde 1996. É a escolha padrão para APIs Node no mercado — robusto, gratuito e compatível com o SQL padrão.

```text
Por que Postgres e não "qualquer banco"?
├─ Gratuito e open source — sem licença
├─ SQL padrão — o que você aprende vale para outros bancos
├─ Recursos avançados — JSONB, índices parciais, CTEs
└─ Usado por startups e gigantes — habilidade empregável
```

## Arquitetura

```text
┌─────────────┐   ┌─────────────┐
│   psql      │   │  sua API    │     clientes
│  (terminal) │   │  (Prisma)   │
└──────┬──────┘   └──────┬──────┘
       └────────┬────────┘
                ▼ porta 5432
       ┌─────────────────┐
       │  Servidor       │
       │  PostgreSQL     │
       │ ┌─────────────┐ │
       │ │  postgres   │ │  ← banco default
       │ │  meu_banco  │ │  ← seus bancos
       │ └─────────────┘ │
       └─────────────────┘
```

- **Um servidor** hospeda **vários bancos de dados** independentes
- Clientes conectam na porta `5432` (padrão)
- `postgres` é o banco default, criado na instalação

## Formas de interagir

| Ferramenta | Tipo | Quando usar |
| --- | --- | --- |
| `psql` | Linha de comando | Scripts, servidor remoto, rapidez |
| pgAdmin | GUI oficial | Explorar visualmente, administração |
| DBeaver / DataGrip | GUI universal | Trabalhar com vários SGBDs |
| Prisma/ORM | Via código | A aplicação em si |

## String de conexão

Aplicações conectam via URL:

```text
postgresql://usuario:senha@host:porta/banco
postgresql://postgres:1234@localhost:5432/meubanco
```

É exatamente esse formato que o Prisma usa no `DATABASE_URL`.

## Convenções do Postgres

- **Case**: nomes de tabelas/colunas ficam em minúsculas — use `snake_case`
- `SELECT "Nome"` com aspas duplas força case-sensitive — evite
- Strings com **aspas simples**: `WHERE nome = 'Ana'`
- Identificadores com **aspas duplas** (quando necessário): `"minhaTabela"`

## psql — primeiros comandos

```bash
psql -U postgres          # conecta
```

```sql
\l                -- lista bancos
\c meu_banco      -- troca de banco
\dt               -- lista tabelas do banco atual
\d usuarios       -- estrutura da tabela
\x                -- saída expandida (liga/desliga)
\timing           -- mostra tempo das queries
\q                -- sai
```

Comandos `\` são do **psql** (cliente), não do SQL — não precisam de `;`.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `password authentication failed` | Senha errada ou `pg_hba.conf` exige `md5` |
| `database "x" does not exist` | Liste com `\l` e crie com `CREATE DATABASE` |
| Aspas duplas em string | `'Ana'` — aspas duplas são para identificadores |
| `Maiúscula` em nome de tabela | Postgres dobra para minúsculas — use `snake_case` |

## Resumo

- PostgreSQL = SGBD relacional open source, padrão de mercado para APIs
- Um servidor na porta 5432 hospeda vários bancos independentes
- `psql` no terminal, pgAdmin na GUI, ORM na aplicação
- `postgresql://user:pass@host:5432/db` é o formato de conexão que os ORMs usam
