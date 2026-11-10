# BE02-04 — Instalação: PostgreSQL no macOS

## Opção 1 — Homebrew (recomendada)

```bash
brew install postgresql@16
brew services start postgresql@16
```

O `brew services` registra o PostgreSQL para iniciar com o login.

## Opção 2 — Postgres.app

App gráfico em `postgresapp.com` — baixe, arraste para Applications, abra e clique em **Start**. Simples, sem configuração, ideal para quem não quer mexer no terminal na instalação.

## PATH (Homebrew)

O PostgreSQL via brew pode não entrar no PATH sozinho:

```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Em Macs Intel o caminho é `/usr/local/opt/postgresql@16/bin`.

## Verificando

```bash
psql --version
psql postgres    # conecta no banco padrão
```

```sql
SELECT version();
\q
```

## Usuário padrão

Diferente do Linux, no macOS o brew cria o superusuário com **seu nome de usuário do sistema** — não existe `postgres` separado nem senha por padrão:

```bash
whoami           # seu usuário
psql -U $(whoami) -d postgres
```

Para criar o usuário `postgres` tradicional:

```sql
CREATE USER postgres WITH PASSWORD 'postgres' SUPERUSER;
```

## Comandos úteis do psql

```sql
\l          -- lista bancos
\c banco    -- conecta em outro banco
\dt         -- lista tabelas
\q          -- sai
```

## Gerenciando o serviço

```bash
brew services list                    # status de todos
brew services stop postgresql@16      # parar
brew services restart postgresql@16   # reiniciar
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `psql: command not found` | PATH não configurado — veja seção acima |
| `role "postgres" does not exist` | No brew o superusuário é seu usuário do macOS |
| `connection refused` | `brew services start postgresql@16` |
| Banco `postgres` não existe | `createdb postgres` ou `initdb` no diretório de dados |

## Resumo

- `brew install postgresql@16` + `brew services start` resolve no macOS
- Postgres.app é a alternativa sem terminal
- O superusuário padrão é o **seu usuário do macOS**, não `postgres`
- Confirme com `psql postgres` e `SELECT version()`
