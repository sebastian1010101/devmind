# BE02-10 — Criando, Selecionando e Excluindo Banco de Dados

## Criar

```sql
CREATE DATABASE meu_banco;
```

```sql
-- com opções
CREATE DATABASE loja
  WITH OWNER = meu_usuario
       ENCODING = 'UTF8';
```

Nomes: minúsculas, `snake_case`, sem espaços nem acentos.

## Listar e conectar

```sql
\l                    -- lista todos os bancos do servidor
\c meu_banco          -- conecta (muda o banco atual)
```

```text
postgres=# \c meu_banco
You are now connected to database "meu_banco" as user "postgres".
meu_banco=#            ← o prompt mostra onde você está
```

Todo comando SQL roda **no banco conectado** — confira o prompt antes de criar tabelas.

## Via terminal, sem entrar no psql

```bash
createdb -U postgres meu_banco    # cria
dropdb -U postgres meu_banco      # exclui
psql -U postgres -d meu_banco     # conecta direto num banco
```

## Excluir

```sql
DROP DATABASE meu_banco;
```

```sql
DROP DATABASE IF EXISTS meu_banco;   -- sem erro se não existe
```

**Cuidados**:

- Não pode dropar o banco em que você está conectado — conecte em `postgres` primeiro
- Não pode dropar banco **com conexões ativas** — encerre as sessões

```sql
-- forçando desconexão de outros clientes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'meu_banco' AND pid <> pg_backend_pid();

DROP DATABASE meu_banco;
```

## Fluxo típico de um projeto

```text
1. psql -U postgres            → entra no banco default
2. CREATE DATABASE minha_api;  → cria o banco do projeto
3. \c minha_api                → conecta nele
4. CREATE TABLE ...            → cria as tabelas
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `database is being accessed by other users` | Conexões abertas — encerre-as ou use `pg_terminate_backend` |
| `cannot drop the currently open database` | `\c postgres` antes de dropar |
| Criou tabela no banco errado | Confira o prompt — `meu_banco=#` |
| `permission denied to create database` | Usuário sem `CREATEDB` — use `postgres` ou `ALTER USER x CREATEDB` |

## Resumo

- `CREATE DATABASE nome` / `DROP DATABASE nome` — com `IF EXISTS` para segurança
- `\c banco` troca o banco conectado; o prompt do psql mostra onde você está
- `createdb`/`dropdb`/`psql -d` funcionam direto do terminal
- Não se dropa banco conectado nem com sessões ativas
