# BE01-31 — Métodos HTTP e Códigos de Status

## Os métodos (verbos)

| Método | Ação | Corpo | Idempotente |
| --- | --- | --- | --- |
| `GET` | Ler recurso(s) | não | ✅ |
| `POST` | Criar | sim | ❌ |
| `PUT` | Substituir inteiro | sim | ✅ |
| `PATCH` | Atualizar parcial | sim | ✅ |
| `DELETE` | Remover | não | ✅ |

**Idempotente** = executar 1x ou 10x dá o mesmo resultado. `DELETE /users/3` repetido não cria 10 deleções.

## PUT vs PATCH

```text
PUT   /usuarios/1  → substitui o recurso INTEIRO (manda tudo)
PATCH /usuarios/1  → altera só os campos enviados
```

```json
// PATCH { "nome": "Novo Nome" } — só o nome muda
// PUT   exige todos os campos — o que faltar vira null/default
```

PATCH é o padrão para atualizações de API — PUT é raro na prática.

## Códigos de status — as famílias

| Faixa | Significado |
| --- | --- |
| `2xx` | Sucesso |
| `3xx` | Redirecionamento |
| `4xx` | Erro do **cliente** |
| `5xx` | Erro do **servidor** |

## Os que você usará todo dia

| Código | Quando |
| --- | --- |
| `200 OK` | GET/PATCH/DELETE com sucesso |
| `201 Created` | POST criou o recurso |
| `204 No Content` | sucesso sem corpo (DELETE) |
| `400 Bad Request` | dados inválidos/ausentes |
| `401 Unauthorized` | sem autenticação |
| `403 Forbidden` | autenticado mas sem permissão |
| `404 Not Found` | recurso não existe |
| `409 Conflict` | conflito (email já cadastrado) |
| `422 Unprocessable` | sintaxe ok, regra de negócio falhou |
| `500 Internal` | erro inesperado do servidor |

## 401 vs 403 — a confusão clássica

- `401` — "quem é você?" → token ausente/inválido
- `403` — "sei quem é você, mas não pode" → sem permissão

## Resumo

- Verbo = ação; URL = recurso; status = resultado
- PATCH para parcial, PUT para substituição total
- 2xx sucesso, 4xx culpa do cliente, 5xx culpa do servidor
- Status correto = API que se explica
