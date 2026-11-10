# BE02-15 — Exclusão de Dados

## DELETE básico

```sql
DELETE FROM usuarios WHERE id = 1;
```

## A regra de ouro (de novo)

```sql
-- ⚠️ SEM WHERE = apaga TODAS as linhas
DELETE FROM usuarios;
```

```sql
-- fluxo seguro:
SELECT * FROM usuarios WHERE id = 1;   -- confirma o alvo
DELETE FROM usuarios WHERE id = 1;     -- mesmo WHERE
```

## Deletando várias linhas

```sql
DELETE FROM logs WHERE criado_em < NOW() - INTERVAL '90 days';
DELETE FROM sessoes WHERE usuario_id = 42;
DELETE FROM carrinho WHERE usuario_id = 7 AND produto_id = 3;
```

## RETURNING

```sql
DELETE FROM usuarios WHERE id = 1 RETURNING *;
```

Devolve o que foi removido — a API usa para confirmar ou responder `204`.

## DELETE vs TRUNCATE vs DROP

| | `DELETE` | `TRUNCATE` | `DROP TABLE` |
| --- | --- | --- | --- |
| O que faz | Remove linhas (filtrável) | Remove **todas** as linhas | Destrói a tabela |
| WHERE | Sim | Não | Não |
| Reseta SERIAL | Não | `RESTART IDENTITY` | — |
| Velocidade em tabela grande | Mais lento (linha a linha) | Instantâneo | Instantâneo |

```sql
TRUNCATE TABLE logs RESTART IDENTITY;
```

## FK — o bloqueio de integridade

```sql
-- usuarios tem pedidos ligados por FK:
DELETE FROM usuarios WHERE id = 1;
-- ERROR: update or delete violates foreign key constraint
```

O banco **impede** deixar pedidos órfãos. Suas opções:

```sql
-- 1. deletar filhos primeiro
DELETE FROM pedidos WHERE cliente_id = 1;
DELETE FROM usuarios WHERE id = 1;

-- 2. ou a FK foi criada com ação referencial:
cliente_id INT REFERENCES usuarios(id) ON DELETE CASCADE
-- aí deletar o usuário já remove os pedidos
```

## Soft delete — alternativa ao DELETE

Em vez de apagar, **marca como inativo**:

```sql
ALTER TABLE usuarios ADD COLUMN deletado_em TIMESTAMPTZ;

UPDATE usuarios SET deletado_em = NOW() WHERE id = 1;   -- "delete"
SELECT * FROM usuarios WHERE deletado_em IS NULL;        -- lista "vivos"
```

| Hard delete | Soft delete |
| --- | --- |
| Dado some de vez | Dado fica, recuperável |
| Libera espaço | Mantém histórico e auditoria |
| Mais simples | Queries precisam filtrar `deletado_em IS NULL` |

Soft delete é padrão quando há auditoria, recuperação ou dados que outras tabelas referenciam.

## Erros comuns

| Erro | Correção |
| --- | --- |
| DELETE sem WHERE | Apagou tudo — filtre sempre |
| FK violada ao deletar | Delete os filhos primeiro ou use `ON DELETE CASCADE` |
| `TRUNCATE` com FK apontando pra tabela | `TRUNCATE ... CASCADE` ou delete manual |
| Esperar que SERIAL reinicie | `TRUNCATE RESTART IDENTITY` ou `ALTER SEQUENCE RESTART` |

## Resumo

- `DELETE FROM tabela WHERE cond` — sem WHERE apaga tudo
- `RETURNING` confirma o que saiu
- FKs protegem contra órfãos — ordem de exclusão importa
- Soft delete (`deletado_em`) é a alternativa quando o dado precisa ser recuperável
