# BE01-32 — CRUD: Create, Read, Update e Delete

## CRUD sobre HTTP

| Operação | Endpoint | Status típico |
| --- | --- | --- |
| Create | `POST /produtos` | `201` |
| Read (lista) | `GET /produtos` | `200` |
| Read (um) | `GET /produtos/:id` | `200` ou `404` |
| Update | `PATCH /produtos/:id` | `200` ou `404` |
| Delete | `DELETE /produtos/:id` | `204` ou `404` |

## O ciclo de cada operação

### Create

```text
POST /produtos  { "nome": "Mouse", "preco": 79.9 }
   ↓ valida body
   ↓ cria no "banco"
201  { "id": 1, "nome": "Mouse", "preco": 79.9 }
```

Erros: `400` (body inválido), `409` (duplicado).

### Read

```text
GET /produtos         → 200 [ {...}, {...} ]
GET /produtos/42      → 200 {...}  ou  404
GET /produtos?cat=x   → 200 filtrado
```

### Update

```text
PATCH /produtos/42  { "preco": 59.9 }
   ↓ existe? não → 404
   ↓ valida parcial → inválido → 400
   ↓ aplica
200  { recurso atualizado }
```

### Delete

```text
DELETE /produtos/42
   ↓ existe? não → 404
   ↓ remove
204  (sem corpo)
```

## Onde cada camada mora

```text
Rota (Express)     → define método + caminho
Middleware         → valida body, autentica
Controller         → recebe req, chama service, monta res
Service            → regra de negócio
"Database"         → array em memória → Prisma (módulo 07)
```

## Erros por operação

| Operação | Erros comuns |
| --- | --- |
| Create | `400` validação, `409` conflito |
| Read um | `404` não existe |
| Update | `404` + `400` validação |
| Delete | `404` |

## Idempotência no CRUD

- `POST` não é idempotente — retry duplica o recurso (double submit)
- `GET`/`PATCH`/`DELETE` são — retry é seguro
- Proteja o create: chave de idempotência ou constraint única no banco

## Resumo

- As 5 rotas REST cobrem o CRUD inteiro
- Cada operação tem seu par de sucesso/erro (201/400, 200/404, 204/404)
- PATCH = parcial; POST não é idempotente
- A estrutura já é a mesma do BE01-14 — agora exposta via HTTP
