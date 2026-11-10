# BE02-18 — Relacionamento 1-1

## Conceito

Um registro da tabela A se liga a **no máximo um** registro da tabela B, e vice-versa.

```text
usuario ──────── perfil
   1      tem      1
```

Casos de uso: separar dados pouco acessados (bio, avatar), dados sensíveis (documentos), ou estender uma tabela sem alterá-la.

## Implementação — FK + UNIQUE

A diferença para o 1-N é o **`UNIQUE` na chave estrangeira** — impede dois perfis apontando para o mesmo usuário:

```sql
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE perfis (
  id SERIAL PRIMARY KEY,
  bio TEXT,
  avatar_url VARCHAR(500),
  usuario_id INT UNIQUE NOT NULL REFERENCES usuarios(id)
);
```

Sem o `UNIQUE`, `usuario_id` poderia se repetir — viraria 1-N.

## Qual lado carrega a FK?

```text
usuarios ──(1:1)── perfis
```

A FK vai na tabela **"filha"** — aquela que não existe sozinha. Um perfil sem usuário não faz sentido; um usuário sem perfil, sim.

Regra prática: a FK vai na tabela cuja existência **depende** da outra.

## Alternativa — PK compartilhada

A PK do filho **é** a FK (o perfil tem o mesmo id do usuário):

```sql
CREATE TABLE perfis (
  usuario_id INT PRIMARY KEY REFERENCES usuarios(id),
  bio TEXT,
  avatar_url VARCHAR(500)
);
```

Mais enxuto (sem `id` redundante) e o 1-1 é garantido pela própria PK. Ambas as formas são válidas — a segunda é mais rigorosa.

## Consultando

```sql
SELECT u.nome, p.bio, p.avatar_url
FROM usuarios u
JOIN perfis p ON p.usuario_id = u.id;
```

```text
      nome      |        bio
----------------+------------------
 Ana            | dev backend
 Bruno          | data analyst
```

## Quando usar vs coluna na mesma tabela

| Colocar em `usuarios` | Tabela `perfis` separada |
| --- | --- |
| Poucos campos, sempre usados | Muitos campos, raramente lidos |
| Dados essenciais | Dados opcionais/sensíveis |
| Mais simples (sem JOIN) | Mantém `usuarios` enxuta |

Se o perfil tem 3 campos, uma coluna extra em `usuarios` costuma bastar. 1-1 real vale para blocos grandes ou com regras de acesso diferentes.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Esquecer `UNIQUE` na FK | Sem ele vira 1-N — dois perfis por usuário |
| FK na tabela errada | FK vai no lado que depende (perfil depende de usuário) |
| Deletar usuário deixando perfil órfão | `ON DELETE CASCADE` na FK |
| Criar 1-1 para 2 colunas | Avalie — colunas extras na tabela bastam |

## Resumo

- 1-1 = FK com `UNIQUE` (ou PK compartilhada) no lado dependente
- Um usuário, um perfil; uma pessoa, um passaporte
- Útil para separar dados opcionais, grandes ou sensíveis — não para qualquer agrupamento
- `ON DELETE CASCADE` evita órfãos quando o pai some
