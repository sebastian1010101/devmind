# BE02-24 — Join: Parte 2

## JOIN com mais de duas tabelas

Cenário: pedidos que envolvem cliente, itens e produtos.

```text
clientes ──< pedidos ──< itens_pedido >── produtos
```

```sql
SELECT
  c.nome AS cliente,
  p.id AS pedido,
  pr.nome AS produto,
  i.quantidade,
  i.quantidade * pr.preco AS subtotal
FROM itens_pedido i
JOIN pedidos  p  ON p.id = i.pedido_id
JOIN clientes c ON c.id = p.cliente_id
JOIN produtos pr ON pr.id = i.produto_id
ORDER BY p.id;
```

```text
cliente │ pedido │ produto  │ quantidade │ subtotal
────────┼────────┼──────────┼────────────┼──────────
Ana     │   10   │ Teclado  │     1      │  250.00
Ana     │   10   │ Mouse    │     2      │  100.00
```

## JOIN com cálculo e alias

Colunas calculadas funcionam normal — `quantidade * preco`, `UPPER(nome)`, concatenação:

```sql
SELECT
  c.nome || ' (pedido #' || p.id || ')' AS descricao,
  SUM(i.quantidade * pr.preco) AS total
FROM itens_pedido i
JOIN pedidos p  ON p.id = i.pedido_id
JOIN clientes c ON c.id = p.cliente_id
JOIN produtos pr ON pr.id = i.produto_id
GROUP BY c.nome, p.id;
```

## JOIN através de tabela intermediária (N-N)

O caminho N-N usa a junção como ponte:

```sql
SELECT e.nome AS estudante, c.titulo AS curso
FROM matriculas m
JOIN estudantes e ON e.id = m.estudante_id
JOIN cursos c     ON c.id = m.curso_id;
```

```text
estudante │ curso
──────────┼────────
Ana       │ SQL
Ana       │ React
Bruno     │ SQL
```

## Filtrando junto com JOIN

`WHERE` se aplica **depois** do JOIN:

```sql
SELECT l.titulo, a.nome
FROM livros l
JOIN autores a ON a.id = l.autor_id
WHERE a.pais = 'Brasil'
ORDER BY l.titulo;
```

## Self join — tabela que se relaciona consigo

Funcionários e seus gerentes, na mesma tabela:

```sql
CREATE TABLE funcionarios (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  gerente_id INT REFERENCES funcionarios(id)
);
```

```sql
SELECT f.nome AS funcionario, g.nome AS gerente
FROM funcionarios f
LEFT JOIN funcionarios g ON g.id = f.gerente_id;
```

A mesma tabela entra duas vezes com **dois apelidos** (`f` e `g`) — sem alias é impossível distinguir.

## ON vs WHERE no filtro

```sql
-- condição no ON: filtra o casamento
JOIN pedidos p ON p.id = i.pedido_id AND p.status = 'pago'

-- condição no WHERE: filtra o resultado final
WHERE p.status = 'pago'
```

No `INNER JOIN` os dois são equivalentes. Em `LEFT JOIN` **diferem** — condição no `WHERE` pode anular o efeito do LEFT (transformando-o em INNER na prática).

## Erros comuns

| Erro | Correção |
| --- | --- |
| 3 tabelas com JOIN pulando a ponte | Siga o encadeamento de FKs — `i → p → c` |
| Self join sem dois apelidos | `FROM funcionarios f JOIN funcionarios g` |
| Condição errada no WHERE com LEFT JOIN | Mova para o `ON` se quer preservar nulos |
| Somar sem GROUP BY | `SUM` com colunas normais exige `GROUP BY` |

## Resumo

- 3+ tabelas = encadear JOINs seguindo as FKs — sem atalhos
- N-N consulta sempre passa pela intermediária
- Self join: mesma tabela, dois apelidos (`funcionario`/`gerente`)
- No `INNER`, `ON` e `WHERE` equivalente; no `LEFT`, posição do filtro muda o resultado
