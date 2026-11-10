# BE02-07 — Chaves Primárias e Chaves Estrangeiras

## Chave primária (PK)

A **chave primária** identifica unicamente cada linha da tabela. Regras:

- Única — duas linhas nunca têm o mesmo valor
- Não nula — sempre existe
- Imutável — não deve mudar (por isso `id` artificial é preferido a CPF/email)

```sql
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL
);
```

### PK natural vs surrogate

| Tipo | Exemplo | Quando usar |
| --- | --- | --- |
| Surrogate (artificial) | `id SERIAL` | Quase sempre — simples, imutável |
| Natural | CPF, ISBN | Quando o dado é realmente único e estável |

```sql
-- chave composta: duas colunas juntas identificam a linha
PRIMARY KEY (estudante_id, curso_id)
```

## Chave estrangeira (FK)

A **chave estrangeira** liga uma tabela a outra — garante **integridade referencial**: não existe pedido de cliente que não existe.

```sql
CREATE TABLE pedidos (
  id SERIAL PRIMARY KEY,
  cliente_id INT NOT NULL REFERENCES usuarios(id),
  total NUMERIC(10,2)
);
```

`cliente_id REFERENCES usuarios(id)` = "todo `cliente_id` aqui precisa existir como `id` lá".

```sql
-- ERRO: usuário 99 não existe → o banco recusa
INSERT INTO pedidos (cliente_id, total) VALUES (99, 50.00);
-- ERROR: violates foreign key constraint
```

## Ações referenciais — o que acontece ao deletar

```sql
CREATE TABLE pedidos (
  id SERIAL PRIMARY KEY,
  cliente_id INT REFERENCES usuarios(id) ON DELETE CASCADE
);
```

| Ação | Ao deletar o pai... |
| --- | --- |
| `RESTRICT`/`NO ACTION` (padrão) | Bloqueia — não deleta usuário com pedidos |
| `CASCADE` | Deleta os filhos junto — usuário e seus pedidos |
| `SET NULL` | Filho fica órfão com `NULL` (FK precisa ser nullable) |

```sql
ON DELETE CASCADE ON UPDATE CASCADE
```

## Constraints relacionadas

```sql
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,   -- UNIQUE = chave candidata
  cpf CHAR(11) UNIQUE
);
```

- `UNIQUE` — sem duplicatas, mas aceita `NULL` (diferente de PK)
- `NOT NULL` — obrigatório
- `PRIMARY KEY` = `UNIQUE` + `NOT NULL` + identidade da linha

## Visualizando

```text
usuarios                    pedidos
┌────┬───────┐              ┌────┬────────────┬───────┐
│ id │ nome  │◄─────────────│ id │ cliente_id │ total │
├────┼───────┤   FK         ├────┼────────────┼───────┤
│  1 │ Ana   │              │ 10 │     1      │ 99.90 │
│  2 │ Bruno │              │ 11 │     1      │ 25.00 │
└────┴───────┘              │ 12 │     2      │ 10.00 │
                            └────┴────────────┴───────┘
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Inserir filho antes do pai | Insira `usuarios` antes de `pedidos` |
| Deletar pai com filhos | Escolha `CASCADE`, `SET NULL` ou delete filhos antes |
| PK que muda (email como PK) | Use `SERIAL`/UUID surrogate |
| FK apontando para coluna não-única | FK precisa referenciar PK ou coluna `UNIQUE` |

## Resumo

- PK identifica a linha: única, não-nula, estável — `SERIAL` é o padrão
- FK garante integridade referencial: o valor precisa existir na tabela pai
- `ON DELETE CASCADE/SET NULL/RESTRICT` definem o comportamento ao deletar
- `UNIQUE` marca chaves candidatas (email, cpf) sem ser a PK
