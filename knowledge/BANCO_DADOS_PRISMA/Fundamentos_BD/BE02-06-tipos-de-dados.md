# BE02-06 — Tipos de Dados

## Por que o tipo importa

O tipo da coluna define o que pode ser guardado, quanto espaço ocupa e quais operações existem. Tipo certo = integridade + performance.

## Numéricos

| Tipo | Tamanho | Uso |
| --- | --- | --- |
| `SMALLINT` | 2 bytes | Contadores pequenos (-32k a 32k) |
| `INTEGER` / `INT` | 4 bytes | Ids, quantidades — padrão geral |
| `BIGINT` | 8 bytes | Números gigantes |
| `SERIAL` | 4 bytes | Int **auto-incremento** — típico de PK |
| `NUMERIC(p,s)` / `DECIMAL` | variável | **Dinheiro** — exato: `NUMERIC(10,2)` |
| `REAL` / `DOUBLE PRECISION` | 4/8 bytes | Ponto flutuante — aproximado, evite para dinheiro |

```sql
preco NUMERIC(10,2)   -- até 99999999.99, sem erro de arredondamento
```

`FLOAT`/`REAL` guardam aproximações — `0.1 + 0.2 ≠ 0.3`. Dinheiro é sempre `NUMERIC`/`DECIMAL`.

## Texto

| Tipo | Uso |
| --- | --- |
| `VARCHAR(n)` | Texto com limite — `VARCHAR(255)` para emails |
| `CHAR(n)` | Tamanho fixo — `CHAR(2)` para sigla de estado |
| `TEXT` | Texto sem limite — descrições, conteúdo |

No PostgreSQL, `VARCHAR` sem tamanho e `TEXT` têm a mesma performance — o limite do `VARCHAR(n)` serve como validação.

## Booleano

```sql
ativo BOOLEAN   -- TRUE, FALSE ou NULL
```

Aceita literais: `TRUE`/`FALSE`, `'t'`/`'f'`, `'yes'`/`'no'`, `1`/`0`.

## Data e hora

| Tipo | Guarda |
| --- | --- |
| `DATE` | Só data — `2026-09-27` |
| `TIME` | Só hora — `14:30:00` |
| `TIMESTAMP` | Data + hora — `2026-09-27 14:30:00` |
| `TIMESTAMPTZ` | Timestamp **com fuso** — preferível em APIs |

```sql
criado_em TIMESTAMPTZ DEFAULT NOW()
```

`TIMESTAMPTZ` normaliza para UTC — evita caos quando servidor e usuário estão em fusos diferentes.

## Outros úteis

| Tipo | Uso |
| --- | --- |
| `UUID` | Identificadores únicos universais — `gen_random_uuid()` |
| `JSON` / `JSONB` | Dados semi-estruturados — `JSONB` é indexável |
| `VARCHAR` para senha | **Nunca** texto puro — guarde o hash (bcrypt) |

```sql
id UUID DEFAULT gen_random_uuid() PRIMARY KEY
```

## Montando uma tabela real

```sql
CREATE TABLE produtos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  descricao TEXT,
  preco NUMERIC(10,2) NOT NULL CHECK (preco >= 0),
  estoque INT DEFAULT 0,
  ativo BOOLEAN DEFAULT TRUE,
  criado_em TIMESTAMPTZ DEFAULT NOW()
);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Dinheiro em `FLOAT` | Use `NUMERIC(10,2)` — flutuante arredonda |
| Telefone/CPF em `INT` | Use `VARCHAR` — zeros à esquerda se perdem |
| Data em `VARCHAR` | Use `DATE`/`TIMESTAMP` — texto não ordena nem compara |
| `TIMESTAMP` sem fuso em API | Prefira `TIMESTAMPTZ` |
| Senha em texto | Guarde hash bcrypt — nunca a senha |

## Resumo

- `INT`/`SERIAL` para ids, `NUMERIC` para dinheiro exato
- `VARCHAR(n)` com limite, `TEXT` sem limite — mesma performance no Postgres
- `TIMESTAMPTZ` para APIs; `BOOLEAN` nativo existe — não use `INT` 0/1
- Tipo errado (dinheiro em float, data em texto) causa bugs silenciosos
