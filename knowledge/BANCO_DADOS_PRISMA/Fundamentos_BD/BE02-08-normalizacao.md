# BE02-08 — Normalização

## O problema que resolve

Normalização é o processo de **organizar tabelas para eliminar redundância e anomalias**. Dado duplicado é dado que pode ficar inconsistente.

```text
Anomalias de uma tabela mal modelada:
├─ Inserção:  não dá pra cadastrar curso sem estudante
├─ Atualização: mudar nome do curso exige atualizar N linhas
└─ Exclusão:  deletar o último estudante apaga o curso junto
```

## Tabela desnormalizada — o exemplo base

```text
matriculas
┌────┬───────────┬─────────────────┬──────────────┬───────────┐
│ id │ estudante │ email_estudante │ curso        │ instrutor │
├────┼───────────┼─────────────────┼──────────────┼───────────┤
│  1 │ Ana       │ ana@mail.com    │ SQL Básico   │ Carlos    │
│  2 │ Ana       │ ana@mail.com    │ React        │ Paula     │
│  3 │ Bruno     │ bruno@mail.com  │ SQL Básico   │ Carlos    │
└────┴───────────┴─────────────────┴──────────────┴───────────┘
```

Ana se repete. "SQL Básico" e "Carlos" se repetem. Mudou o email da Ana? Atualize várias linhas — e se esquecer uma, inconsistente.

## 1ª Forma Normal (1NF)

**Regra**: valores atômicos — uma coluna, um valor. Nada de listas na célula.

```text
❌ telefones = "9999-1111, 9999-2222"
✅ uma linha por telefone OU tabela telefones separada
```

Também exige: cada linha identificável (PK) e sem grupos de colunas repetidas (`telefone1`, `telefone2`, `telefone3`).

## 2ª Forma Normal (2NF)

**Regra**: estar em 1NF + todo atributo não-chave depende da **chave inteira** — só se aplica a chaves compostas.

```text
matriculas (PK: estudante_id + curso_id)
├─ data_matricula   ← depende dos dois ✅
├─ nome_estudante   ← depende só de estudante_id ❌
└─ nome_curso       ← depende só de curso_id ❌
```

Dependência parcial → extraia para sua própria tabela.

## 3ª Forma Normal (3NF)

**Regra**: estar em 2NF + atributo não-chave não depende de **outro atributo não-chave** (dependência transitiva).

```text
matriculas
├─ curso       ← depende de id
└─ instrutor   ← depende de curso, não de id ❌
```

`instrutor` é fato sobre `curso`, não sobre a matrícula → vai para a tabela `cursos`.

## O resultado normalizado

```sql
CREATE TABLE estudantes (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE cursos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  instrutor VARCHAR(100)
);

CREATE TABLE matriculas (
  estudante_id INT REFERENCES estudantes(id),
  curso_id INT REFERENCES cursos(id),
  data_matricula DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (estudante_id, curso_id)
);
```

Cada fato em um lugar só. Mudou o email da Ana? Uma linha, uma vez.

## Quando desnormalizar

Normalização **não é dogma**. Relatórios que precisam de muitos JOINs podem justificar duplicação controlada:

| Normalizado | Desnormalizado |
| --- | --- |
| Sem redundância, sempre consistente | Mais rápido para leitura |
| JOINs nas consultas | Menos JOINs |
| Padrão para sistemas transacionais | Comum em relatórios/analytics |

Desnormalize **conscientemente**, por performance medida — não por preguiça de modelar.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Lista separada por vírgula numa célula | Viola 1NF — linha por valor |
| Atributo que depende de metade da PK composta | Viola 2NF — extraia a tabela |
| `cidade` guardando também `estado` junto | Viola 3NF se estado depende de cidade |
| Normalizar tudo até 5NF "porque sim" | 3NF resolve 99% dos casos reais |

## Resumo

- Normalização elimina redundância → elimina anomalias de insert/update/delete
- 1NF: valores atômicos; 2NF: sem dependência parcial de chave composta; 3NF: sem dependência transitiva
- Resultado típico: uma tabela por entidade, ligadas por FKs
- Desnormalizar é ferramenta de performance, não padrão
