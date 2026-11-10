# BE02-28 — Group By e Having

## GROUP BY — agregando por grupo

Sozinha, agregação resume a tabela inteira. `GROUP BY` quebra em **grupos** — uma linha de resultado por valor distinto:

```sql
SELECT cidade, COUNT(*) AS total
FROM usuarios
GROUP BY cidade;
```

```text
cidade │ total
───────┼───────
SP     │  15
RJ     │   8
BH     │   4
```

"Quantos usuários **por cidade**" — a coluna do GROUP BY define os baldes.

## A regra fundamental

Toda coluna no `SELECT` deve ser ou **agregada** ou estar no `GROUP BY`:

```sql
-- ✅ cidade está no GROUP BY, COUNT é agregada
SELECT cidade, COUNT(*) FROM usuarios GROUP BY cidade;

-- ❌ nome não está nem agregado nem no GROUP BY
SELECT cidade, nome, COUNT(*) FROM usuarios GROUP BY cidade;
-- ERROR: column "nome" must appear in the GROUP BY clause
```

Faz sentido: cada grupo tem uma cidade, mas "o nome" de quem? Ambíguo.

## Múltiplas colunas no GROUP BY

```sql
SELECT cidade, estado, COUNT(*)
FROM usuarios
GROUP BY cidade, estado;   -- um grupo por combinação cidade+estado
```

## HAVING — filtro DEPOIS de agregar

`WHERE` não vê agregados — executa antes. Para filtrar grupos, `HAVING`:

```sql
-- cidades com mais de 10 usuários
SELECT cidade, COUNT(*) AS total
FROM usuarios
GROUP BY cidade
HAVING COUNT(*) > 10;
```

```text
WHERE  → filtra LINHAS antes de agrupar
HAVING → filtra GRUPOS depois de agregar
```

## WHERE + GROUP BY + HAVING juntos

```sql
SELECT cliente_id, SUM(total) AS gasto
FROM pedidos
WHERE status = 'pago'           -- 1. só pedidos pagos
GROUP BY cliente_id             -- 2. agrupa por cliente
HAVING SUM(total) > 500         -- 3. só quem gastou mais de 500
ORDER BY gasto DESC;            -- 4. ordena pelo total
```

## Ordem lógica de execução (completa)

```text
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

Por isso:

- `WHERE` não aceita `COUNT()` — ainda não existe
- `HAVING` não aceita alias do `SELECT` — ainda não existe (use a expressão)

## Exemplos combinados

```sql
-- autores com 3+ livros
SELECT a.nome, COUNT(l.id) AS livros
FROM autores a
JOIN livros l ON l.autor_id = a.id
GROUP BY a.nome
HAVING COUNT(l.id) >= 3;

-- categoria com ticket médio alto
SELECT categoria, AVG(preco) AS media
FROM produtos
GROUP BY categoria
HAVING AVG(preco) > 100
ORDER BY media DESC;
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Coluna fora do GROUP BY | Ou agrega (`MAX(nome)`), ou adiciona no GROUP BY, ou tira |
| `WHERE COUNT(*) > 10` | Agregado no WHERE é inválido — use `HAVING` |
| `HAVING total > 10` com alias | Alguns bancos aceitam, Postgres não — repita `COUNT(*)` |
| Grupo errado por coluna a mais | `GROUP BY cidade` ≠ `GROUP BY cidade, estado` |
| COUNT com JOIN explodindo | JOIN multiplica linhas — conte `COUNT(DISTINCT x)` se inflar |

## Resumo

- `GROUP BY col` cria um grupo por valor; agregações rodam por grupo
- Regra: coluna no SELECT está agregada ou no GROUP BY
- `WHERE` filtra linhas antes; `HAVING` filtra grupos depois
- Ordem mental: `WHERE → GROUP BY → HAVING → ORDER BY`
