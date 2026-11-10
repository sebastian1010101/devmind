# BE02-21 — Relacionamento N-N

## Conceito

Vários registros de A se ligam a vários de B — e vice-versa.

```text
estudante >──────< curso
    N     faz      N
```

Um estudante faz muitos cursos; um curso tem muitos estudantes.

## Por que não dá direto

```sql
-- ❌ colocar curso_id em estudantes: um estudante = um curso só
-- ❌ colocar array de ids: viola 1NF, impossível dar JOIN
```

Nenhuma das duas tabelas pode carregar a ligação sozinha.

## Solução — tabela intermediária

Cria-se uma terceira tabela (**junção** ou *junction*) com duas FKs:

```sql
CREATE TABLE estudantes (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL
);

CREATE TABLE cursos (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL
);

CREATE TABLE matriculas (
  estudante_id INT NOT NULL REFERENCES estudantes(id),
  curso_id INT NOT NULL REFERENCES cursos(id),
  PRIMARY KEY (estudante_id, curso_id)
);
```

```text
estudantes        matriculas          cursos
┌────┬───────┐    ┌──────────────┬──────────┐   ┌────┬───────┐
│ id │ nome  │◄───│ estudante_id │ curso_id │──►│ id │ titulo│
├────┼───────┤    ├──────────────┼──────────┤   ├────┼───────┤
│  1 │ Ana   │    │      1       │    1     │   │  1 │ SQL   │
│  2 │ Bruno │    │      1       │    2     │   │  2 │ React │
└────┴───────┘    │      2       │    1     │   └────┴───────┘
                  └──────────────┴──────────┘
```

## PK composta

`PRIMARY KEY (estudante_id, curso_id)` tem dois efeitos:

1. Identifica a linha pelo **par** — não precisa de `id` próprio
1. **Impede matrícula duplicada** — o par não pode se repetir

Se a ligação tiver atributos próprios, pode-se usar `id SERIAL` + `UNIQUE(a,b)` no lugar.

## Ligações com dados próprios

A tabela intermediária pode guardar atributos da **relação**:

```sql
CREATE TABLE matriculas (
  id SERIAL PRIMARY KEY,
  estudante_id INT NOT NULL REFERENCES estudantes(id),
  curso_id INT NOT NULL REFERENCES cursos(id),
  data_matricula DATE DEFAULT CURRENT_DATE,
  nota NUMERIC(3,1),
  UNIQUE (estudante_id, curso_id)
);
```

`nota` não pertence ao estudante nem ao curso — pertence **à matrícula**. Quando a relação tem dados, ela é uma entidade.

## Consultando — dois JOINs

```sql
-- cursos de um estudante
SELECT c.titulo
FROM matriculas m
JOIN cursos c ON c.id = m.curso_id
WHERE m.estudante_id = 1;

-- estudantes de um curso
SELECT e.nome
FROM matriculas m
JOIN estudantes e ON e.id = m.estudante_id
WHERE m.curso_id = 1;
```

O caminho sempre passa pela intermediária: `A → junção → B`.

## Erros comuns

| Erro | Correção |
| --- | --- |
| FK direta entre as duas tabelas | N-N exige intermediária — FK direta vira 1-N |
| Sem PK composta/UNIQUE | Matrículas duplicadas passam |
| Atributo da relação na tabela errada | `nota` vai em `matriculas`, não em `estudantes` |
| JOIN direto entre as pontas | Sempre `A JOIN junção JOIN B` |

## Resumo

- N-N não existe direto — resolve com **tabela intermediária** e 2 FKs
- PK composta `(a_id, b_id)` identifica e impede duplicatas
- A intermediária pode virar entidade própria quando tem atributos (data, nota, status)
- Consultas cruzam por dois JOINs: A → junção → B
