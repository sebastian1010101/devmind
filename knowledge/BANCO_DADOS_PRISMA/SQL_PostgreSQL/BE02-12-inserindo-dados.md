# BE02-12 — Inserindo Dados

## INSERT básico

```sql
INSERT INTO usuarios (nome, email, idade)
VALUES ('Ana', 'ana@mail.com', 28);
```

- Liste as colunas **explicitamente** — a ordem dos `VALUES` segue a ordem declarada
- Strings usam **aspas simples** — `'Ana'`
- Colunas com `DEFAULT`/`SERIAL` podem ser omitidas

## Múltiplas linhas

```sql
INSERT INTO usuarios (nome, email, idade) VALUES
  ('Bruno', 'bruno@mail.com', 34),
  ('Carla', 'carla@mail.com', 22),
  ('Diego', 'diego@mail.com', 41);
```

Um `INSERT` com vários `VALUES` é **muito** mais rápido que N inserts separados — uma transação, um round-trip.

## RETURNING — recebendo o que foi criado

```sql
INSERT INTO usuarios (nome, email)
VALUES ('Elena', 'elena@mail.com')
RETURNING id, criado_em;
```

```text
 id |          criado_em
----+------------------------------
  5 | 2026-09-27 10:15:30.123-03
```

Sem `RETURNING`, você não sabe qual `id` o `SERIAL` gerou — a API precisa disso para devolver o objeto criado.

## Omitindo vs explícito

```sql
-- perigoso: depende da ordem das colunas da tabela
INSERT INTO usuarios VALUES (DEFAULT, 'Ana', 'ana@mail.com', 28, NOW());

-- seguro: colunas nomeadas — sobrevive a ALTER TABLE
INSERT INTO usuarios (nome, email, idade) VALUES ('Ana', 'ana@mail.com', 28);
```

## INSERT ... SELECT — copiando dados

```sql
INSERT INTO usuarios_backup (id, nome, email)
SELECT id, nome, email FROM usuarios WHERE ativo = false;
```

Insere o resultado de uma query em outra tabela — útil para backups e migrações.

## Conflitos — ON CONFLICT

```sql
-- email é UNIQUE: segunda inserção falharia
INSERT INTO usuarios (nome, email)
VALUES ('Ana', 'ana@mail.com')
ON CONFLICT (email) DO NOTHING;         -- ignora o conflito

-- upsert: insere ou atualiza
INSERT INTO usuarios (nome, email, idade)
VALUES ('Ana', 'ana@mail.com', 29)
ON CONFLICT (email) DO UPDATE SET idade = EXCLUDED.idade;
```

`EXCLUDED` refere-se aos valores que **seriam** inseridos.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `duplicate key value violates unique constraint` | Email já existe — trate com `ON CONFLICT` |
| `null value violates not-null constraint` | Coluna obrigatória omitida — inclua no INSERT ou dê `DEFAULT` |
| `column "x" does not exist` | Typo no nome ou a coluna não foi criada |
| `value too long for type character varying(100)` | String maior que o limite do `VARCHAR` |
| VALUES fora de ordem | Sempre nomeie as colunas explicitamente |

## Resumo

- `INSERT INTO tabela (cols) VALUES (...)` — sempre liste as colunas
- Múltiplos `VALUES` num insert só: mais rápido e atômico
- `RETURNING` devolve id e campos gerados — essencial para APIs
- `ON CONFLICT DO NOTHING / DO UPDATE` trata duplicatas e faz upsert
