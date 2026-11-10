# BE02-27 — Funções de Agregação

## Conceito

Funções que **resumem várias linhas num valor só**:

```sql
SELECT COUNT(*) FROM usuarios;        -- quantas linhas
SELECT SUM(total) FROM pedidos;       -- soma
SELECT AVG(preco) FROM produtos;      -- média
SELECT MIN(preco), MAX(preco) FROM produtos;  -- extremos
```

## As principais

| Função | Retorna | Ignora NULL? |
| --- | --- | --- |
| `COUNT(*)` | Nº de linhas | — |
| `COUNT(col)` | Nº de não-nulos na coluna | Sim |
| `COUNT(DISTINCT col)` | Nº de valores distintos | Sim |
| `SUM(col)` | Soma | Sim |
| `AVG(col)` | Média | Sim |
| `MIN(col)` / `MAX(col)` | Menor / maior | Sim |

## COUNT — as nuances

```sql
SELECT COUNT(*) FROM usuarios;            -- todas as linhas
SELECT COUNT(telefone) FROM usuarios;     -- só quem tem telefone
SELECT COUNT(DISTINCT cidade) FROM usuarios;  -- cidades diferentes
```

`COUNT(*)` conta linhas; `COUNT(coluna)` pula `NULL`s — diferença sutil mas importa.

## Exemplos práticos

```sql
-- faturamento total
SELECT SUM(total) FROM pedidos WHERE status = 'pago';

-- ticket médio
SELECT AVG(total) FROM pedidos;

-- produto mais barato e mais caro
SELECT MIN(preco) AS menor, MAX(preco) AS maior FROM produtos;

-- pedidos por cliente
SELECT cliente_id, COUNT(*) AS pedidos, SUM(total) AS gasto
FROM pedidos
GROUP BY cliente_id;
```

## Agregação + filtro

`WHERE` filtra **antes** de agregar:

```sql
SELECT AVG(nota) FROM avaliacoes WHERE aprovado = true;
```

Para filtrar **depois** de agregar, existe `HAVING` (próxima aula).

## Agregação com JOIN

```sql
SELECT c.nome, COUNT(p.id) AS total_pedidos
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.nome;
```

`LEFT JOIN` + `COUNT(p.id)` (não `*`) — cliente sem pedido conta `0` corretamente.

## NULL e agregação — pegadinhas

```sql
SELECT AVG(desconto) FROM pedidos;
-- desconto NULL não entra na média!
-- média calculada sobre menos linhas do que você espera
```

```sql
SELECT AVG(COALESCE(desconto, 0)) FROM pedidos;  -- NULL vira 0
```

`COALESCE(col, valor)` substitui NULL — útil quando NULL deveria significar "zero".

## Erros comuns

| Erro | Correção |
| --- | --- |
| `COUNT(col)` contando menos que o esperado | NULLs são ignorados — `COUNT(*)` ou `COALESCE` |
| `SELECT nome, COUNT(*)` sem GROUP BY | Coluna comum + agregada exige `GROUP BY` |
| `WHERE` tentando filtrar agregado | `WHERE` roda antes — agregado filtra com `HAVING` |
| `AVG` retornando inteiro | `AVG(INT)` vira numeric; se truncar, `AVG(x::numeric)` |
| Contar filhos com INNER JOIN | Pais sem filhos somem — `LEFT JOIN` + `COUNT(fk)` |

## Resumo

- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` resumem linhas num valor
- `COUNT(*)` conta linhas; `COUNT(col)` pula NULLs; `DISTINCT` conta únicos
- `WHERE` filtra antes de agregar; `HAVING` filtra depois
- `COALESCE(col, 0)` resolve o problema de NULL na média
