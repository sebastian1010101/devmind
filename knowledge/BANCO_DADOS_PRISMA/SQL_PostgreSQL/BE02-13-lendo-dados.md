# BE02-13 — Lendo Dados

## SELECT básico

```sql
SELECT * FROM usuarios;                  -- todas as colunas
SELECT nome, email FROM usuarios;        -- colunas específicas
```

Evite `SELECT *` em produção — traga só o que precisa (rede, memória, índices).

## WHERE — filtrando

```sql
SELECT * FROM usuarios WHERE idade >= 18;
SELECT * FROM usuarios WHERE email = 'ana@mail.com';
SELECT * FROM usuarios WHERE ativo = true AND idade > 25;
SELECT * FROM usuarios WHERE cidade = 'SP' OR cidade = 'RJ';
```

### Operadores úteis

```sql
WHERE idade BETWEEN 18 AND 30           -- intervalo inclusivo
WHERE cidade IN ('SP', 'RJ', 'MG')      -- lista de valores
WHERE nome LIKE 'Ana%'                  -- começa com Ana
WHERE nome ILIKE '%ana%'                -- contém "ana", ignora case
WHERE telefone IS NULL                  -- nulo (nunca use = NULL)
WHERE telefone IS NOT NULL
```

- `LIKE`: `%` = qualquer sequência, `_` = um caractere
- `ILIKE` = `LIKE` case-insensitive — específico do Postgres
- `NULL` só se compara com `IS` — `= NULL` é sempre falso

## ORDER BY — ordenando

```sql
SELECT * FROM usuarios ORDER BY nome;              -- A→Z
SELECT * FROM usuarios ORDER BY criado_em DESC;    -- mais recentes
SELECT * FROM usuarios ORDER BY idade DESC, nome;  -- desempate
```

## LIMIT e OFFSET — paginação

```sql
SELECT * FROM usuarios ORDER BY id LIMIT 10;           -- página 1
SELECT * FROM usuarios ORDER BY id LIMIT 10 OFFSET 10; -- página 2
```

Sempre combine `LIMIT` com `ORDER BY` — sem ordenação, "os 10 primeiros" é imprevisível.

## DISTINCT — sem duplicatas

```sql
SELECT DISTINCT cidade FROM usuarios;
SELECT DISTINCT ON (cidade) * FROM usuarios ORDER BY cidade, id;  -- Postgres
```

## Alias — apelidando

```sql
SELECT nome AS usuario, email AS contato FROM usuarios;
SELECT u.nome FROM usuarios u;          -- alias de tabela (útil em JOINs)
```

## Funções no SELECT

```sql
SELECT nome, EXTRACT(YEAR FROM data_nascimento) AS ano FROM usuarios;
SELECT UPPER(nome), LENGTH(nome) FROM usuarios;
SELECT nome || ' <' || email || '>' AS formatado FROM usuarios;  -- concatenação
```

## Ordem lógica de execução

```text
FROM → WHERE → SELECT → DISTINCT → ORDER BY → LIMIT/OFFSET
```

Por isso não dá para usar alias do `SELECT` no `WHERE` — o WHERE executa antes.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `WHERE ativo = 'true'` | Boolean é `ativo = true` (sem aspas) |
| `NULL = NULL` retorna vazio | Use `IS NULL` |
| `LIKE 'ana'` acha nada | Sem `%`, LIKE equivale a `=` |
| LIMIT sem ORDER BY | Página inconsistente — sempre ordene |
| Alias do SELECT no WHERE | Repita a expressão ou use subquery |

## Resumo

- `SELECT cols FROM tabela WHERE cond ORDER BY col LIMIT n`
- `IN`, `BETWEEN`, `LIKE`/`ILIKE`, `IS NULL` cobrem os filtros comuns
- Paginação = `LIMIT` + `OFFSET` + `ORDER BY` obrigatório
- Strings com aspas simples, boolean com `true`/`false`, nulo com `IS`
