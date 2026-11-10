# BE02-11 — Criando e Excluindo Tabelas

## CREATE TABLE

```sql
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  idade INT CHECK (idade >= 0),
  criado_em TIMESTAMPTZ DEFAULT NOW()
);
```

Anatomia:

```text
CREATE TABLE nome_da_tabela (
  coluna  TIPO  constraints,
  coluna  TIPO  constraints,
  ...
);
```

## Constraints de coluna

| Constraint | Efeito |
| --- | --- |
| `PRIMARY KEY` | Identifica a linha (única + não nula) |
| `NOT NULL` | Obrigatória — rejeita `NULL` |
| `UNIQUE` | Sem valores repetidos |
| `DEFAULT x` | Valor automático quando omitido |
| `CHECK (condição)` | Validação customizada |
| `REFERENCES tabela(col)` | Chave estrangeira |

## Constraint de tabela

Quando envolve mais de uma coluna, declara-se no final:

```sql
CREATE TABLE matriculas (
  estudante_id INT REFERENCES estudantes(id),
  curso_id INT REFERENCES cursos(id),
  data DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (estudante_id, curso_id),          -- PK composta
  UNIQUE (estudante_id, curso_id, data)          -- constraint nomeável
);
```

## Inspecionando

```sql
\dt              -- lista tabelas
\d usuarios      -- colunas, tipos, constraints, índices
```

## ALTER TABLE — modificando

```sql
ALTER TABLE usuarios ADD COLUMN telefone VARCHAR(20);
ALTER TABLE usuarios DROP COLUMN telefone;
ALTER TABLE usuarios ALTER COLUMN nome TYPE VARCHAR(150);
ALTER TABLE usuarios ALTER COLUMN email SET NOT NULL;
ALTER TABLE usuarios ADD CONSTRAINT email_unico UNIQUE (email);
ALTER TABLE usuarios RENAME COLUMN nome TO nome_completo;
ALTER TABLE usuarios RENAME TO users;
```

## Excluindo

```sql
DROP TABLE usuarios;
DROP TABLE IF EXISTS usuarios;
DROP TABLE usuarios CASCADE;   -- remove junto quem depende dela (FKs)
```

`CASCADE` deleta as **constraints** dependentes — não as linhas das outras tabelas.

## TRUNCATE vs DROP

```sql
TRUNCATE TABLE usuarios;              -- esvazia, a tabela continua existindo
TRUNCATE TABLE usuarios RESTART IDENTITY;  -- zera o SERIAL também
DROP TABLE usuarios;                  -- a tabela deixa de existir
```

| | `DELETE` | `TRUNCATE` | `DROP` |
| --- | --- | --- | --- |
| Remove linhas | Sim (ou parte) | Todas | Todas |
| Mantém a tabela | Sim | Sim | **Não** |
| Reseta SERIAL | Não | Com `RESTART IDENTITY` | — |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `relation "x" already exists` | Tabela já criada — `DROP TABLE` antes ou use outro nome |
| `cannot drop table because other objects depend` | `DROP TABLE x CASCADE` ou delete as tabelas filhas antes |
| Mudar tipo com dados incompatíveis | `ALTER COLUMN x TYPE novo USING x::novo` |
| Esquecer `IF NOT EXISTS` em script | `CREATE TABLE IF NOT EXISTS x (...)` torna reexecutável |

## Resumo

- `CREATE TABLE` define colunas com tipo + constraints (`NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`, `REFERENCES`)
- Constraints de tabela no final cobrem PKs compostas
- `ALTER TABLE` adiciona/remove/modifica colunas e constraints sem recriar
- `TRUNCATE` esvazia, `DROP` destrói — saiba a diferença
