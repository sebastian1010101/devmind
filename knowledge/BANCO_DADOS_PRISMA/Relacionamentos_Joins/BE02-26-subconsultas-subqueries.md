# BE02-26 — Subconsultas (Subqueries)

## Conceito

Uma **query dentro de outra query** — o resultado interno alimenta o externo:

```sql
SELECT nome FROM produtos
WHERE preco > (SELECT AVG(preco) FROM produtos);
```

```text
1. (SELECT AVG(preco))   → 150.00
2. SELECT ... WHERE preco > 150.00
```

O Postgres executa **de dentro pra fora**.

## Subquery no WHERE

```sql
-- produtos mais caros que a média
SELECT nome, preco FROM produtos
WHERE preco > (SELECT AVG(preco) FROM produtos);

-- livros do Machado
SELECT titulo FROM livros
WHERE autor_id = (SELECT id FROM autores WHERE nome = 'Machado de Assis');
```

Subquery de **valor único** — usa operadores normais (`=`, `>`, `<`).

## IN — subquery de lista

```sql
-- autores que TÊM livros
SELECT nome FROM autores
WHERE id IN (SELECT autor_id FROM livros);

-- autores SEM livros
SELECT nome FROM autores
WHERE id NOT IN (SELECT autor_id FROM livros);
```

`IN` recebe uma lista de valores — a subquery retorna N linhas, uma coluna.

## EXISTS — teste de existência

```sql
SELECT nome FROM autores a
WHERE EXISTS (
  SELECT 1 FROM livros l WHERE l.autor_id = a.id
);
```

`EXISTS` responde "existe alguma linha que casa?" — costuma ser mais rápido que `IN` em tabelas grandes, porque para no primeiro resultado.

## Subquery no SELECT — coluna calculada

```sql
SELECT
  nome,
  (SELECT COUNT(*) FROM livros l WHERE l.autor_id = a.id) AS total_livros
FROM autores a;
```

Cada linha de `autores` executa a subquery — vira uma coluna do resultado. Funciona, mas `JOIN` + `GROUP BY` costuma ser mais legível e rápido.

## Subquery no FROM — tabela derivada

```sql
SELECT categoria, media
FROM (
  SELECT categoria, AVG(preco) AS media
  FROM produtos
  GROUP BY categoria
) AS medias
WHERE media > 100;
```

A subquery vira uma "tabela temporária" que a query externa consulta. **Exige alias** (`AS medias`).

## Subquery correlacionada

Quando a interna referencia a externa — executa **uma vez por linha**:

```sql
SELECT nome FROM produtos p
WHERE preco > (
  SELECT AVG(preco) FROM produtos
  WHERE categoria = p.categoria     -- referência à externa
);
```

"média da **mesma** categoria" — poderosa, mas pode ser lenta (N execuções).

## Subquery vs JOIN

```sql
-- equivalentes:
SELECT nome FROM autores WHERE id IN (SELECT autor_id FROM livros);

SELECT DISTINCT a.nome
FROM autores a JOIN livros l ON l.autor_id = a.id;
```

| Subquery | JOIN |
| --- | --- |
| Lê como linguagem natural | Combina colunas das duas tabelas |
| Boa para filtros e existência | Boa para trazer dados relacionados |
| Pode ser mais lenta correlacionada | Otimizador costuma lidar melhor |

Regra prática: filtro/existência → subquery ou `EXISTS`; trazer colunas da outra tabela → JOIN.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `=` com subquery de várias linhas | Use `IN` — `=` exige valor único |
| Subquery no FROM sem alias | `) AS apelido` é obrigatório |
| `NOT IN` com NULL na lista | NULL contamina — prefira `NOT EXISTS` |
| Correlacionada lenta em tabela grande | Avalie reescrever com JOIN/GROUP BY |

## Resumo

- Subquery = query dentro de query; executa de dentro pra fora
- `WHERE x IN (SELECT...)`, `EXISTS`, valor único com `=`/`>`
- No `SELECT` vira coluna calculada; no `FROM` vira tabela derivada (exige alias)
- Correlacionada roda por linha — JOIN/GROUP BY costuma ser alternativa melhor
