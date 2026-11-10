# BE02-19 — Relacionamento 1-N

## Conceito

Um registro da tabela A se liga a **muitos** registros da tabela B; cada B pertence a **um** A.

```text
autor ───────< livro
  1    escreve   N
```

É o relacionamento mais comum: usuário→pedidos, categoria→produtos, post→comentários.

## Implementação — FK no lado N

A chave estrangeira vai **sempre no lado "muitos"** — cada livro aponta para seu autor:

```sql
CREATE TABLE autores (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL
);

CREATE TABLE livros (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  autor_id INT NOT NULL REFERENCES autores(id)
);
```

```text
autores              livros
┌────┬────────┐      ┌────┬───────────────┬──────────┐
│ id │ nome   │◄─────│ id │ titulo        │ autor_id │
├────┼────────┤      ├────┼───────────────┼──────────┤
│  1 │ Machado│      │  1 │ Dom Casmurro  │    1     │
│  2 │ Amado  │      │  2 │ Brás Cubas    │    1     │
└────┴────────┘      │  3 │ Cap. Areia    │    2     │
                     └────┴───────────────┴──────────┘
```

## Populando

```sql
INSERT INTO autores (nome) VALUES ('Machado de Assis'), ('Jorge Amado');

INSERT INTO livros (titulo, autor_id) VALUES
  ('Dom Casmurro', 1),
  ('Memórias Póstumas de Brás Cubas', 1),
  ('Capitães da Areia', 2);
```

**Ordem importa**: o autor precisa existir antes dos livros que o referenciam.

## Consultando com JOIN

```sql
SELECT l.titulo, a.nome AS autor
FROM livros l
JOIN autores a ON a.id = l.autor_id;
```

```text
             titulo              |      autor
---------------------------------+------------------
 Dom Casmurro                    | Machado de Assis
 Memórias Póstumas de Brás Cubas | Machado de Assis
 Capitães da Areia               | Jorge Amado
```

## Operações no sentido inverso

```sql
-- quantos livros cada autor tem
SELECT a.nome, COUNT(l.id) AS total_livros
FROM autores a
LEFT JOIN livros l ON l.autor_id = a.id
GROUP BY a.nome;
```

`LEFT JOIN` garante que autor **sem** livro também apareça (com `0`).

## Deletando o pai

```sql
DELETE FROM autores WHERE id = 1;
-- ERROR: livros ainda apontam para ele
```

Escolha a ação referencial na FK:

| Ação | Efeito ao deletar autor |
| --- | --- |
| Padrão (`NO ACTION`) | Bloqueia enquanto houver livros |
| `ON DELETE CASCADE` | Apaga os livros junto |
| `ON DELETE SET NULL` | Livros ficam com `autor_id = NULL` |

Para `SET NULL`, a FK não pode ser `NOT NULL`.

## Erros comuns

| Erro | Correção |
| --- | --- |
| FK no lado "um" | `autor` com `livro_id`? Errado — FK vai no N |
| Inserir livro antes do autor | Insira o pai primeiro — FK exige existência |
| `INNER JOIN` escondendo pais sem filhos | `LEFT JOIN` para incluir autor sem livro |
| Array de ids no pai (`livro_ids = "{1,2}"`) | Viola normalização — FK é no filho |

## Resumo

- 1-N: o lado N carrega a FK que aponta para o lado 1
- Insira o pai antes dos filhos; o banco garante a integridade
- `LEFT JOIN` inclui pais sem filhos; `JOIN` só mostra pares existentes
- `ON DELETE CASCADE`/`SET NULL` definem o destino dos filhos ao deletar o pai
