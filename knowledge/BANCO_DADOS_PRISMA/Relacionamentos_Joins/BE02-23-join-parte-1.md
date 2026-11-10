# BE02-23 — Join: Parte 1

## O problema que o JOIN resolve

Os dados estão separados em tabelas normalizadas — mas as respostas que queremos cruzam tabelas:

```text
"nome do cliente + total do pedido" → clientes + pedidos
"título do livro + nome do autor"   → livros + autores
```

`JOIN` combina linhas de tabelas diferentes **numa única resposta**, casando-as pela condição `ON`.

## INNER JOIN — o padrão

```sql
SELECT l.titulo, a.nome AS autor
FROM livros l
JOIN autores a ON a.id = l.autor_id;
```

```text
livros ⋈ autores
┌───────────────┬──────────────────┐
│ titulo        │ autor            │
├───────────────┼──────────────────┤
│ Dom Casmurro  │ Machado de Assis │
│ Cap. Areia    │ Jorge Amado      │
└───────────────┴──────────────────┘
```

Só entram no resultado as linhas que **casam** — livro sem autor válido não aparece, autor sem livro também não.

## Anatomia

```sql
SELECT  colunas (de qualquer tabela)
FROM    tabela_a  [apelido]
JOIN    tabela_b  ON condição_de_ligação
WHERE   filtros
ORDER BY ...
```

- `ON` define o casamento — quase sempre `fk = pk`
- Apelidos (`l`, `a`) deixam a query legível
- `JOIN` sozinho = `INNER JOIN`

## Qualificando colunas ambíguas

```sql
SELECT l.id, l.titulo, a.nome
FROM livros l JOIN autores a ON a.id = l.autor_id;
--        ↑
-- "id" existe nas duas — precisa do prefixo l./a.
```

`id` sozinho dá erro de ambiguidade: `column reference "id" is ambiguous`.

## JOIN implícito — forma antiga

```sql
-- funciona, mas NÃO use
SELECT l.titulo, a.nome
FROM livros l, autores a
WHERE l.autor_id = a.id;
```

Funciona, mas mistura ligação com filtro e facilita o esquecimento do `WHERE` (produto cartesiano — cada linha × cada linha). Prefira sempre `JOIN ... ON`.

## Múltiplos JOINs

Encadeie para cruzar 3+ tabelas:

```sql
SELECT p.id, c.nome AS cliente, pr.nome AS produto, i.quantidade
FROM itens_pedido i
JOIN pedidos p  ON p.id = i.pedido_id
JOIN clientes c ON c.id = p.cliente_id
JOIN produtos pr ON pr.id = i.produto_id;
```

Cada `JOIN` adiciona uma tabela à combinação — a ordem não importa para o resultado.

## Produto cartesiano — o erro clássico

```sql
SELECT * FROM livros, autores;   -- sem condição
-- 10 livros × 5 autores = 50 linhas sem sentido
```

`CROSS JOIN` faz isso **de propósito** (combinações) — mas fora desse caso, cartesiano = bug.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `column "id" is ambiguous` | Prefixe: `l.id`, `a.id` |
| Resultado gigante sem sentido | Faltou o `ON` — produto cartesiano |
| Sintaxe `FROM a, b WHERE...` | Reescreva com `JOIN ... ON` explícito |
| Linha sumindo | INNER só mostra casamentos — veja LEFT JOIN |

## Resumo

- `JOIN` combina tabelas numa resposta, casando por `ON fk = pk`
- `INNER JOIN` (padrão): só pares que existem dos dois lados
- Prefixe colunas ambíguas com o apelido da tabela
- Sem `ON` você cria produto cartesiano — quase sempre um bug
