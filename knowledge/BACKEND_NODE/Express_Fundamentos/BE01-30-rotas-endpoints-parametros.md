# BE01-30 — Rotas, Endpoints e Parâmetros de Requisição

## Rota e endpoint

- **Rota** — o caminho: `/usuarios`, `/produtos/:id`
- **Endpoint** — método + caminho: `GET /usuarios`, `DELETE /produtos/3`

O mesmo caminho com métodos diferentes são endpoints diferentes:

```text
GET    /produtos      → listar todos
POST   /produtos      → criar
GET    /produtos/:id  → buscar um
PATCH  /produtos/:id  → atualizar
DELETE /produtos/:id  → remover
```

## Os 3 lugares onde dados chegam

### 1. Route params — identifica o recurso

```text
GET /usuarios/42
         └─ req.params.id = "42"  (sempre string!)
```

### 2. Query string — filtra/ordena/pagina

```text
GET /produtos?categoria=eletronicos&ordem=preco&pagina=2
              └─ req.query = { categoria: "eletronicos", ordem: "preco", pagina: "2" }
```

### 3. Body — dados do recurso (POST/PATCH)

```json
POST /usuarios
{
  "nome": "Ana",
  "email": "ana@email.com"
}
```

## Quando usar cada um

| Dado | Onde |
| --- | --- |
| Qual recurso (`/usuarios/42`) | route param |
| Filtro, busca, página, ordenação | query string |
| Conteúdo criado/atualizado | body |
| Token, idioma, content-type | headers |

## Convenções de URL

```text
✅ /usuarios          recurso no plural
✅ /usuarios/42       param identifica um recurso
✅ /usuarios/42/pedidos   sub-recursos aninhados
❌ /listarUsuarios    verbo na URL (o verbo é o método HTTP)
❌ /usuario           singular
```

A URL é substantivo (o recurso); o método HTTP é o verbo (a ação).

## Resumo

- Endpoint = método + caminho; params identificam, query filtra, body carrega dados
- Params e query chegam como **strings** — converta/valide antes de usar
- URL = substantivo plural; ação = método HTTP
