# BE02-25 — Joins: Inner, Left, Right, Full

## Os quatro tipos

```text
A          B
┌───┐    ┌───┐
│   │    │   │
│ A │ B  │ B │      INNER: só A∩B
│   │    │   │      LEFT:  todo A + B que casa
└───┘    └───┘      RIGHT: todo B + A que casa
                    FULL:  tudo dos dois lados
```

## Cenário

```text
autores                    livros
┌────┬─────────┐           ┌────┬───────────┬──────────┐
│ id │ nome    │           │ id │ titulo    │ autor_id │
├────┼─────────┤           ├────┼───────────┼──────────┤
│  1 │ Machado │           │  1 │ Casmurro  │    1     │
│  2 │ Amado   │           │  2 │ Cap.Areia │    2     │
│  3 │ Le Guin │ (sem livro)│ 3 │ Órfão     │   NULL   │
└────┴─────────┘           └────┴───────────┴──────────┘
```

## INNER JOIN — só os casamentos

```sql
SELECT a.nome, l.titulo
FROM autores a
INNER JOIN livros l ON l.autor_id = a.id;
```

```text
nome    │ titulo
────────┼───────────
Machado │ Casmurro
Amado   │ Cap.Areia
```

Le Guin (sem livro) e "Órfão" (sem autor) **ficam de fora**.

## LEFT JOIN — tudo da esquerda

```sql
SELECT a.nome, l.titulo
FROM autores a
LEFT JOIN livros l ON l.autor_id = a.id;
```

```text
nome    │ titulo
────────┼───────────
Machado │ Casmurro
Amado   │ Cap.Areia
Le Guin │ NULL          ← sem livro, mas aparece
```

Todo autor aparece; quem não tem livro vem com `NULL` nas colunas de `livros`.

**Uso clássico** — achar quem **não** tem filhos:

```sql
SELECT a.nome
FROM autores a
LEFT JOIN livros l ON l.autor_id = a.id
WHERE l.id IS NULL;          -- só os sem livro
```

## RIGHT JOIN — tudo da direita

```sql
SELECT a.nome, l.titulo
FROM autores a
RIGHT JOIN livros l ON l.autor_id = a.id;
```

```text
nome    │ titulo
────────┼───────────
Machado │ Casmurro
Amado   │ Cap.Areia
NULL    │ Órfão          ← livro sem autor aparece
```

É o LEFT "de trás pra frente" — na prática, quase sempre se prefere reescrever como LEFT trocando a ordem das tabelas.

## FULL OUTER JOIN — tudo dos dois lados

```sql
SELECT a.nome, l.titulo
FROM autores a
FULL OUTER JOIN livros l ON l.autor_id = a.id;
```

```text
nome    │ titulo
────────┼───────────
Machado │ Casmurro
Amado   │ Cap.Areia
Le Guin │ NULL
NULL    │ Órfão
```

União do LEFT + RIGHT: casamentos + sobras de A + sobras de B.

## Resumo visual

```text
INNER:  A∩B          ── só casamentos
LEFT:   A + (A∩B)    ── toda A
RIGHT:  (A∩B) + B    ── toda B
FULL:   A ∪ B        ── tudo
```

| Pergunta | JOIN |
| --- | --- |
| "Livros e seus autores" | INNER |
| "Autores, mesmo sem livro" | LEFT |
| "Livros, mesmo sem autor" | LEFT (livros primeiro) |
| "Só quem NÃO tem vínculo" | LEFT + `WHERE fk IS NULL` |
| "Tudo, dos dois lados" | FULL |

## Erros comuns

| Erro | Correção |
| --- | --- |
| WHERE na tabela da direita anulando o LEFT | `WHERE l.campo = x` descarta os NULLs — use `ON` ou `IS NULL` |
| RIGHT quando dava pra ler melhor com LEFT | Inverta a ordem das tabelas |
| Esperar NULL nas colunas erradas | No LEFT, NULLs ficam nas colunas de **B** |
| FULL em problema de relatório simples | INNER/LEFT resolvem 95% dos casos |

## Resumo

- `INNER` só casamentos; `LEFT`/`RIGHT` preservam um lado com NULL no outro; `FULL` preserva os dois
- `LEFT JOIN + WHERE filho IS NULL` = clássico "quem não tem filhos"
- LEFT domina a prática — RIGHT e FULL são raros
- Filtro no `WHERE` quebra LEFT JOIN: condição na tabela opcional vai pro `ON`
