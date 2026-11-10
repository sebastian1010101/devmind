# BE02-00 — O que é um Banco de Dados

## Definição

Um **banco de dados** é uma coleção organizada de dados, armazenada e acessada eletronicamente. Mais que "guardar informação", ele permite **consultar, atualizar e relacionar** dados de forma eficiente e segura.

```text
Aplicação → SGBD → arquivos de dados em disco
```

## SGBD — o software que gerencia

O **SGBD** (Sistema de Gerenciamento de Banco de Dados, ou DBMS em inglês) é o software entre a aplicação e os dados. Ele cuida de:

- Armazenamento e recuperação dos dados
- Controle de acesso (quem pode ver/alterar o quê)
- Integridade (os dados obedecem regras)
- Concorrência (vários usuários ao mesmo tempo)
- Backup e recuperação de falhas

| SGBD | Tipo | Uso comum |
| --- | --- | --- |
| PostgreSQL | Relacional | APIs, sistemas web (open source) |
| MySQL | Relacional | Web, WordPress, aplicações gerais |
| SQLite | Relacional | Embarcado, mobile, testes |
| MongoDB | Documentos (NoSQL) | Dados flexíveis, JSON-like |
| Redis | Chave-valor (NoSQL) | Cache, sessões |

## Modelo relacional

O modelo mais usado. Dados ficam em **tabelas** (relações):

```text
Tabela: usuarios
┌────┬───────────┬───────────────────────┐
│ id │ nome      │ email                 │  ← colunas (atributos)
├────┼───────────┼───────────────────────┤
│  1 │ Ana       │ ana@mail.com          │  ← linha (registro)
│  2 │ Bruno     │ bruno@mail.com        │
└────┴───────────┴───────────────────────┘
```

- **Tabela**: conjunto de dados sobre uma entidade
- **Coluna**: um atributo (nome, tipo, regras)
- **Linha**: um registro individual
- **SQL**: linguagem padrão para consultar e manipular

## Relacional vs NoSQL

| Relacional (SQL) | Não relacional (NoSQL) |
| --- | --- |
| Esquema fixo e rígido | Esquema flexível |
| Tabelas com relacionamentos | Documentos, chave-valor, grafos |
| Forte em integridade e transações | Forte em escala horizontal e volume |
| PostgreSQL, MySQL | MongoDB, Redis, Cassandra |

Não é "qual é melhor" — é "qual resolve o problema". APIs com dados estruturados e relacionados quase sempre usam relacional.

## Por que não usar só arquivos?

```text
planilha.csv → funciona para 100 linhas, quebra com 1 milhão
```

Arquivos simples falham em:

1. **Concorrência** — dois processos escrevendo ao mesmo tempo corrompem o arquivo
1. **Consultas** — buscar "usuários de SP que compraram em maio" exige ler tudo
1. **Integridade** — nada impede um pedido apontar para um cliente inexistente
1. **Segurança** — sem controle de acesso granular

## Anatomia de uma consulta

```sql
SELECT nome, email
FROM usuarios
WHERE id = 1;
```

- `SELECT` — quais colunas
- `FROM` — de qual tabela
- `WHERE` — filtro das linhas

## Resumo

- Banco de dados = dados organizados + software (SGBD) que os gerencia
- Relacional organiza em tabelas com linhas e colunas; consulta-se em SQL
- PostgreSQL é o SGBD relacional usado no módulo
- SGBD resolve concorrência, integridade, segurança e consultas eficientes — coisas que arquivos simples não fazem
