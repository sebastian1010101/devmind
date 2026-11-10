# BE02-03 — Instalação: PostgreSQL no Linux

## Debian/Ubuntu (apt)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

`postgresql-contrib` traz extensões e utilidades extras — vale instalar junto.

## Verificando o serviço

```bash
sudo systemctl status postgresql
sudo systemctl enable postgresql   # inicia com o boot
sudo systemctl start postgresql    # se não estiver rodando
```

## Primeiro acesso — usuário postgres

O instalador cria um usuário de **sistema** chamado `postgres`, que é o superusuário do banco. O acesso inicial é feito **através dele**:

```bash
sudo -u postgres psql
```

```sql
postgres=# SELECT version();
postgres=# \q    -- sai
```

## Criando seu usuário e banco

Trabalhar como `postgres` o tempo todo é má prática. Crie um usuário seu:

```bash
sudo -u postgres psql
```

```sql
CREATE USER meu_usuario WITH PASSWORD 'minha_senha' CREATEDB;
CREATE DATABASE meu_banco OWNER meu_usuario;
```

Depois conecte direto:

```bash
psql -U meu_usuario -d meu_banco -h localhost
```

## Autenticação — pg_hba.conf

Se der erro `peer authentication failed` ao conectar com seu usuário, o arquivo `pg_hba.conf` controla os métodos de autenticação:

```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

```ini
# troque "peer" por "md5" nas linhas locais
local   all   all   md5
host    all   all   127.0.0.1/32   md5
```

```bash
sudo systemctl restart postgresql
```

- `peer` — usuário do sistema precisa ter o mesmo nome do usuário do banco
- `md5` — autentica por senha (o que a API vai usar)

## Comandos úteis do psql

```sql
\l          -- lista bancos
\c banco    -- conecta em outro banco
\dt         -- lista tabelas
\d tabela   -- descreve uma tabela
\du         -- lista usuários
\q          -- sai
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `peer authentication failed` | Conecte via `sudo -u postgres psql` ou mude `pg_hba.conf` para `md5` |
| `connection refused` | Serviço parado: `sudo systemctl start postgresql` |
| Porta 5432 em uso | Outro PostgreSQL rodando — `sudo lsof -i :5432` |
| `psql: command not found` | Instale `postgresql-client` ou o pacote completo |

## Resumo

- `apt install postgresql postgresql-contrib` instala tudo
- O serviço é gerenciado pelo `systemctl`
- Primeiro acesso sempre via `sudo -u postgres psql`
- Crie usuário próprio com senha e ajuste `pg_hba.conf` para `md5` — é assim que a API conecta
