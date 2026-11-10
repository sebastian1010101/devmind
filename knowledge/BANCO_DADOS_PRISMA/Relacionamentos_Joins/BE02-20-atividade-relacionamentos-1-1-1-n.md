# BE02-20 — Atividade: Praticando Relacionamentos 1-1 e 1-N

## Objetivo

Modelar e implementar um esquema que combine 1-1 e 1-N, povoar com dados e validar com consultas.

## Modelo sugerido — plataforma de cursos

```text
instrutor ──(1:1)── bio_instrutor
instrutor ──(1:N)── curso
curso     ──(1:N)── aula
```

- Um instrutor tem **uma** bio
- Um instrutor ministra **vários** cursos
- Um curso tem **várias** aulas

## Implementação

```sql
CREATE DATABASE plataforma_cursos;
\c plataforma_cursos

CREATE TABLE instrutores (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE bios (
  id SERIAL PRIMARY KEY,
  resumo TEXT,
  linkedin VARCHAR(255),
  instrutor_id INT UNIQUE NOT NULL REFERENCES instrutores(id)
);

CREATE TABLE cursos (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  instrutor_id INT NOT NULL REFERENCES instrutores(id)
);

CREATE TABLE aulas (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  duracao_min INT CHECK (duracao_min > 0),
  curso_id INT NOT NULL REFERENCES cursos(id)
);
```

Detalhes a observar:

- `bios.instrutor_id` tem `UNIQUE` — garante o 1-1
- `cursos.instrutor_id` e `aulas.curso_id` sem `UNIQUE` — permitem o N

## Populando

```sql
INSERT INTO instrutores (nome, email) VALUES
  ('Paula', 'paula@mail.com'),
  ('Carlos', 'carlos@mail.com');

INSERT INTO bios (resumo, linkedin, instrutor_id) VALUES
  ('Dev há 10 anos', 'linkedin.com/in/paula', 1);

INSERT INTO cursos (titulo, instrutor_id) VALUES
  ('SQL do Zero', 1),
  ('React Avançado', 1),
  ('Git Essencial', 2);

INSERT INTO aulas (titulo, duracao_min, curso_id) VALUES
  ('SELECT básico', 30, 1),
  ('JOINs', 45, 1),
  ('Hooks', 40, 2),
  ('Init e commit', 20, 3);
```

## Consultas de validação

```sql
-- cursos de cada instrutor
SELECT i.nome, c.titulo
FROM instrutores i
JOIN cursos c ON c.instrutor_id = i.id;

-- aulas de um curso específico
SELECT titulo, duracao_min FROM aulas WHERE curso_id = 1;

-- instrutor com bio
SELECT i.nome, b.linkedin
FROM instrutores i
JOIN bios b ON b.instrutor_id = i.id;
```

## Testando as regras

```sql
-- deve falhar: segunda bio para o mesmo instrutor
INSERT INTO bios (resumo, instrutor_id) VALUES ('Outra bio', 1);
-- ERROR: duplicate key violates unique constraint

-- deve falhar: aula de curso inexistente
INSERT INTO aulas (titulo, curso_id) VALUES ('X', 99);
-- ERROR: violates foreign key constraint
```

## Critérios de conclusão

1. Três tabelas com as cardinalidades corretas
1. `UNIQUE` no 1-1 validado com erro proposital
1. JOINs retornando dados das tabelas ligadas
1. FK barrando referência inválida

## Resumo

- 1-1 se implementa com `UNIQUE` na FK; 1-N com FK simples no lado N
- Um mesmo esquema mistura os dois tipos — bio (1-1) + cursos (1-N) + aulas (1-N)
- Teste as constraints violando-as de propósito — é a prova de que funcionam
