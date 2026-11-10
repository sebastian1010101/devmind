# BE02-14 — Atualizando Dados

## UPDATE básico

```sql
UPDATE usuarios
SET nome = 'Ana Silva'
WHERE id = 1;
```

```text
UPDATE tabela      → qual tabela
SET col = valor    → o que muda
WHERE condição     → em quais linhas
```

## A regra de ouro

```sql
-- ⚠️ SEM WHERE = atualiza TODAS as linhas da tabela
UPDATE usuarios SET ativo = false;
```

**Sempre escreva o WHERE primeiro.** Um bom hábito:

```sql
-- 1. teste o filtro com SELECT
SELECT * FROM usuarios WHERE id = 1;

-- 2. confirme que são as linhas certas

-- 3. só então o UPDATE com o mesmo WHERE
UPDATE usuarios SET nome = 'Ana Silva' WHERE id = 1;
```

## Múltiplas colunas

```sql
UPDATE usuarios
SET nome = 'Ana Silva',
    email = 'ana.silva@mail.com',
    atualizado_em = NOW()
WHERE id = 1;
```

## Valores calculados

```sql
UPDATE produtos SET preco = preco * 1.10;          -- reajuste de 10%
UPDATE produtos SET estoque = estoque - 1 WHERE id = 7;
UPDATE usuarios SET idade = idade + 1 WHERE EXTRACT(MONTH FROM aniversario) = 9;
```

O lado direito pode referenciar a própria coluna — o valor **antigo** é usado.

## RETURNING

```sql
UPDATE usuarios
SET nome = 'Ana Silva'
WHERE id = 1
RETURNING *;
```

Devolve a linha **depois** da atualização — a API retorna isso no response do `PUT`/`PATCH`.

## UPDATE com condições compostas

```sql
UPDATE pedidos
SET status = 'cancelado'
WHERE status = 'pendente'
  AND criado_em < NOW() - INTERVAL '7 days';
```

## UPDATE a partir de outra tabela

```sql
UPDATE pedidos p
SET total = c.limite
FROM clientes c
WHERE p.cliente_id = c.id AND c.vip = true;
```

## Transação para testar

```sql
BEGIN;
UPDATE usuarios SET ativo = false;   -- esqueceu o WHERE!
SELECT COUNT(*) FROM usuarios WHERE ativo = false;  -- ops, todos
ROLLBACK;                            -- desfaz tudo ✅
```

`BEGIN`/`ROLLBACK` é o cinto de segurança para testar UPDATEs destrutivos.

## Erros comuns

| Erro | Correção |
| --- | --- |
| UPDATE sem WHERE | Atualizou a tabela toda — sempre filtre |
| WHERE errado | Teste com `SELECT` antes |
| Esperar erro quando 0 linhas atualizadas | UPDATE em nada não é erro — use `RETURNING` vazio para detectar |
| Esquecer `atualizado_em` | `DEFAULT NOW()` só vale em INSERT — atualize no SET |

## Resumo

- `UPDATE tabela SET col = valor WHERE cond` — o WHERE é obrigatório na prática
- Teste o filtro com `SELECT` antes; use `BEGIN`/`ROLLBACK` para experimentar
- `RETURNING` devolve a linha atualizada — padrão em APIs
- `SET col = col + 1` usa o valor antigo — para incrementos e cálculos
