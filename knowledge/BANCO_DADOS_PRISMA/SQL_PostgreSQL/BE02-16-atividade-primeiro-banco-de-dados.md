# BE02-16 — Atividade: Criando e Gerenciando Meu Primeiro Banco de Dados

## Objetivo

Colocar em prática o ciclo completo: criar um banco, criar tabelas e rodar as 4 operações (CRUD) via SQL no `psql`.

## Checklist do exercício

```text
1. CREATE DATABASE        → banco criado
2. \c banco               → conectado
3. CREATE TABLE           → tabelas com tipos e constraints
4. INSERT                 → dados de exemplo
5. SELECT / WHERE         → consultas
6. UPDATE                 → alterações
7. DELETE                 → exclusões
```

## Modelo sugerido — biblioteca pessoal

```sql
CREATE DATABASE minha_biblioteca;
\c minha_biblioteca

CREATE TABLE autores (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  pais VARCHAR(50)
);

CREATE TABLE livros (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  ano_publicacao INT CHECK (ano_publicacao > 0),
  autor_id INT REFERENCES autores(id),
  lido BOOLEAN DEFAULT FALSE
);
```

## Populando

```sql
INSERT INTO autores (nome, pais) VALUES
  ('Machado de Assis', 'Brasil'),
  ('Jorge Amado', 'Brasil'),
  ('Ursula K. Le Guin', 'EUA');

INSERT INTO livros (titulo, ano_publicacao, autor_id) VALUES
  ('Dom Casmurro', 1899, 1),
  ('Memórias Póstumas de Brás Cubas', 1881, 1),
  ('Capitães da Areia', 1937, 2),
  ('A Mão Esquerda da Escuridão', 1969, 3);
```

## Consultas para praticar

```sql
-- todos os livros com autor
SELECT * FROM livros;

-- só título e ano
SELECT titulo, ano_publicacao FROM livros;

-- livros não lidos
SELECT titulo FROM livros WHERE lido = false;

-- mais antigos que 1900, ordenados
SELECT titulo, ano_publicacao FROM livros
WHERE ano_publicacao < 1900
ORDER BY ano_publicacao;

-- títulos que contêm "memórias" (case-insensitive)
SELECT titulo FROM livros WHERE titulo ILIKE '%memórias%';
```

## Atualizando e excluindo

```sql
-- marcar como lido
UPDATE livros SET lido = true WHERE id = 1;

-- corrigir ano
UPDATE livros SET ano_publicacao = 1881 WHERE titulo ILIKE '%bras cubas%';

-- remover um livro
DELETE FROM livros WHERE id = 4;

-- verificar estado final
SELECT * FROM livros ORDER BY id;
```

## Validando as constraints

```sql
-- deve falhar: autor inexistente
INSERT INTO livros (titulo, ano_publicacao, autor_id)
VALUES ('Órfão', 2000, 99);
-- ERROR: violates foreign key constraint

-- deve falhar: ano inválido
INSERT INTO livros (titulo, ano_publicacao) VALUES ('X', -50);
-- ERROR: violates check constraint
```

## Critérios de conclusão

1. Banco criado e acessível via `psql`
1. Tabelas com PK, FK, `NOT NULL`, `DEFAULT`, `CHECK`
1. CRUD completo executado sem erros
1. Constraints testadas — os INSERTs inválidos foram barrados

## Resumo

- Atividade consolida o ciclo: `CREATE DATABASE` → `\c` → `CREATE TABLE` → CRUD
- Toda tabela tem PK; tabelas relacionadas têm FK
- Constraints (`CHECK`, `NOT NULL`, FK) devem ser **testadas** — tente violá-las de propósito
- Esse mesmo modelo volta no módulo com Prisma — vale guardar o script
