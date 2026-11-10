# BE02-74 — Render: Criando o Banco de Dados

## Criando o PostgreSQL gerenciado

```text
Dashboard → New → PostgreSQL
├─ Name: minha-api-db
├─ Database: minha_api
├─ User: minha_api_user
├─ Region: Oregon (ou a mais próxima)
└─ Plan: Free
```

Render provisiona o banco — leva um minuto.

## As duas URLs de conexão

Na página do banco, **duas** connection strings:

| URL | Para quem |
| --- | --- |
| **Internal Database URL** | Serviços do Render na mesma região — a API usa esta |
| **External Database URL** | Conexão de fora — seu `psql`/Studio local |

```text
Internal: postgres://user:pass@dpg-xxx-a/minha_api          (host interno)
External: postgres://user:pass@dpg-xxx-a.oregon-postgres.render.com/minha_api
```

A API no Render usa a **internal** — mais rápida e sem sair da rede da plataforma.

## Conectando do seu computador

```bash
psql "postgres://user:pass@dpg-xxx-a.oregon-postgres.render.com/minha_api"
```

```ts
// ou no .env local para apontar o Prisma pro banco remoto
DATABASE_URL="postgres://user:pass@dpg-xxx-a.oregon-postgres.render.com/minha_api"
```

Útil para inspecionar dados de produção — **cuidado**: é o banco real.

## Rodando migrations no banco remoto

```bash
# apontando o .env local para a URL externa
npx prisma migrate deploy
```

`migrate deploy` aplica migrations existentes sem gerar novas — o comando certo para produção (não `migrate dev`).

## SSL na URL externa

Conexões externas exigem SSL:

```text
postgres://...?sslmode=require
```

Alguns clientes pedem o parâmetro explícito — Prisma aceita `sslmode=require` na URL.

## Custos do free tier

- Postgres gratuito expira em ~90 dias — depois precisa de plano pago ou migração
- Backup: `pg_dump` pela URL externa

```bash
pg_dump "postgres://user:pass@host-externo/minha_api" > backup.sql
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| API não conecta | Usar **internal** URL no env do web service |
| psql local falha | URL **external** + `sslmode=require` |
| `migrate dev` em prod | `migrate deploy` — dev gera migrations, deploy só aplica |
| Banco sumiu depois de meses | Free tier expira — backup regular ou plano pago |

## Resumo

- New → PostgreSQL cria o banco gerenciado com 2 URLs
- Internal para a API no Render; external para acesso local (com SSL)
- `prisma migrate deploy` aplica migrations no banco remoto
- Free expira — backup via `pg_dump` pela URL externa
