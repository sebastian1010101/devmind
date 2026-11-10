# BE02-05 — Entidades e Atributos

## Modelagem — do mundo real para tabelas

Antes de criar tabelas, **modela-se** o problema: quais "coisas" o sistema precisa representar e o que se sabe sobre cada uma.

```text
"Um estudante se matricula em cursos"
→ entidades: Estudante, Curso
→ relacionamento: Matrícula
```

## Entidade

Uma **entidade** é algo relevante que o sistema armazena — vira uma **tabela**:

| Mundo real | Entidade (tabela) |
| --- | --- |
| Pessoa que estuda | `estudantes` |
| Produto à venda | `produtos` |
| Pedido feito | `pedidos` |

Cada linha da tabela é uma **instância** (ocorrência) da entidade — um estudante específico, um pedido específico.

## Atributo

**Atributos** são as características da entidade — viram **colunas**:

```text
Entidade: Estudante
├─ id          (identificador)
├─ nome
├─ email
├─ data_nascimento
└─ ativo
```

### Tipos de atributo (modelagem)

| Tipo | Exemplo | Como armazenar |
| --- | --- | --- |
| Simples | nome, email | Uma coluna |
| Composto | endereço (rua, número, cidade) | Várias colunas ou tabela separada |
| Multivalorado | telefones de um cliente | Tabela separada (1-N) |
| Derivado | idade (de data_nascimento) | Geralmente calculado, não armazenado |

### Atributo identificador

Todo registro precisa ser unicamente identificável — o identificador vira a **chave primária**:

```sql
CREATE TABLE estudantes (
  id SERIAL PRIMARY KEY,   -- identificador
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);
```

## Relacionamento entre entidades

Entidades se conectam — "estudante **se matricula em** curso":

```text
ESTUDANTE ──< MATRICULA >── CURSO
   1            N       N      1
```

- **1-1**: pessoa ↔ passaporte
- **1-N**: curso → muitos estudantes matriculados
- **N-N**: estudantes ↔ cursos (resolvido com tabela intermediária)

## Do modelo ao SQL

```text
Modelo conceitual (entidades, atributos, relacionamentos)
    ↓
Modelo lógico (tabelas, colunas, chaves)
    ↓
Modelo físico (CREATE TABLE no PostgreSQL)
```

```sql
CREATE TABLE cursos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  carga_horaria INT
);

CREATE TABLE matriculas (
  id SERIAL PRIMARY KEY,
  estudante_id INT REFERENCES estudantes(id),
  curso_id INT REFERENCES cursos(id),
  data_matricula DATE DEFAULT CURRENT_DATE
);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Colocar lista em uma coluna (`telefones = "111, 222"`) | Atributo multivalorado → tabela separada |
| Armazenar dado derivado (`idade`) | Calcule na query — armazene `data_nascimento` |
| Tabela sem chave primária | Sempre defina `id` ou chave natural única |
| Modelar "de cabeça" sem analisar o domínio | Liste entidades e relacionamentos antes de codar |

## Resumo

- Entidade → tabela; atributo → coluna; instância → linha
- Atributo identificador vira a chave primária
- Multivalorado e composto pedem tabelas/colunas separadas — não liste valores numa célula
- Modele primeiro (conceitual → lógico → físico), depois escreva o `CREATE TABLE`
