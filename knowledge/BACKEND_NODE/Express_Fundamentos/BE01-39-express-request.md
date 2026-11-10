# BE01-39 — Express: Request (req)

## O que é

O objeto que representa **tudo que o cliente enviou** — params, query, body, headers, método, URL.

## As propriedades principais

```typescript
app.post("/usuarios/:id", (req, res) => {
  req.params;    // { id: "42" } — parâmetros da rota
  req.query;     // { pagina: "2" } — ?pagina=2
  req.body;      // { nome: "Ana" } — JSON do corpo (precisa express.json())
  req.headers;   // { authorization: "Bearer ..." } — sempre minúsculos
  req.method;    // "POST"
  req.path;      // "/usuarios/42"
  req.ip;        // IP do cliente
});
```

## `req.params` — identifica o recurso

```typescript
// GET /usuarios/42
req.params.id;           // "42" — STRING sempre
Number(req.params.id);   // 42 — converta antes de comparar
```

## `req.query` — filtros e paginação

```typescript
// GET /produtos?categoria=tech&ordem=preco&pagina=2
const { categoria, ordem, pagina } = req.query;
// tudo string | undefined — opcional por natureza

const paginaNum = Math.max(1, Number(pagina) || 1); // com fallback
```

Query é **opcional** — o cliente pode não mandar. Sempre trate o `undefined`.

## `req.body` — dados enviados

```typescript
// POST /usuarios  { "nome": "Ana", "idade": 28 }
app.use(express.json()); // sem isso, req.body === undefined

req.body.nome;   // "Ana"
req.body.idade;  // 28 — number, pois JSON preserva tipos
```

⚠️ Body é `any` — o TS não sabe o que veio. Validação tipada com Zod em BE01-56.

## `req.headers` — metadados

```typescript
req.headers.authorization;  // "Bearer eyJ..."
req.headers["content-type"];
req.get("Authorization");   // helper case-insensitive
```

Headers ficam em minúsculo no objeto — `req.get()` é o jeito seguro.

## Tipando o Request

```typescript
interface Params { id: string }
interface Body { nome: string }

app.post<{ id: string }, {}, { nome: string }>(
  "/usuarios/:id",
  (req, res) => {
    req.params.id;  // string
    req.body.nome;  // string — tipado
  }
);
```

## O que NÃO vem no req

- `req.user` — não existe nativo; middlewares de auth que criam
- Body parseado — só com `express.json()`/`express.urlencoded()`
- Cookies — só com `cookie-parser`

## Resumo

- `params` = recurso, `query` = filtro opcional, `body` = dados, `headers` = metadados
- Params/query são strings; body preserva tipos JSON
- `express.json()` obrigatório para `req.body`
- `req.get("Header")` para headers — case-insensitive
