# BE02-02 — Instalação: PostgreSQL no Windows

## Download

1. Acesse `postgresql.org/download/windows`
1. Baixe o **instalador EDB** (versão estável mais recente)
1. Execute o `.exe` como administrador

## Wizard de instalação

| Tela | O que fazer |
| --- | --- |
| Diretório de instalação | Padrão `C:\Program Files\PostgreSQL\<versao>` |
| Componentes | Deixe todos: servidor, pgAdmin, Stack Builder, linha de comando |
| Diretório de dados | Padrão (onde os dados ficam fisicamente) |
| **Senha** | Senha do superusuário `postgres` — **anote, você vai precisar** |
| **Porta** | `5432` (padrão) — não mude sem motivo |
| Locale | Padrão do sistema |

## O que foi instalado

- **Servidor PostgreSQL** — roda como serviço do Windows (inicia junto com o SO)
- **psql** — cliente de linha de comando
- **pgAdmin 4** — interface gráfica para administrar o banco

## Verificando a instalação

Abra o **SQL Shell (psql)** no menu iniciar — ele pergunta:

```text
Server [localhost]:        (Enter)
Database [postgres]:       (Enter)
Port [5432]:               (Enter)
Username [postgres]:       (Enter)
Password:                  (sua senha)
```

```sql
SELECT version();
```

Se retornar a versão, está funcionando.

## PATH — psql no terminal comum

Se `psql` não funciona no PowerShell/cmd, adicione ao PATH:

```text
C:\Program Files\PostgreSQL\16\bin
```

Configurações → Sistema → Sobre → Configurações avançadas → Variáveis de ambiente → `Path` → Novo.

## pgAdmin

1. Abra o pgAdmin (roda no navegador)
1. Expanda **Servers → PostgreSQL**
1. Informe a senha do `postgres`
1. Clique com o botão direito em **Databases → Create** para criar um banco

## Erros comuns

| Erro | Correção |
| --- | --- |
| `psql não é reconhecido` | Adicione `...\PostgreSQL\16\bin` ao PATH e reabra o terminal |
| Senha incorreta | É a senha definida no wizard, não a do Windows |
| Porta 5432 em uso | Outro PostgreSQL já instalado — desinstale ou mude a porta |
| Serviço não inicia | `services.msc` → procure `postgresql` → Iniciar |

## Resumo

- Instalador EDB instala servidor + psql + pgAdmin de uma vez
- Senha do superusuário `postgres` e porta `5432` são definidas no wizard
- O servidor roda como serviço do Windows — já inicia sozinho
- Verifique com SQL Shell (psql) ou pelo pgAdmin
