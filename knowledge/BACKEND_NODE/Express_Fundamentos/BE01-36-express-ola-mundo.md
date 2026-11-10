# BE01-36 — Express: Olá Mundo

## O servidor mínimo

```typescript
import express from "express";

const app = express();

app.get("/", (req, res) => {
  res.send("Olá, mundo!");
});

app.listen(3000, () => {
  console.log("🚀 http://localhost:3000");
});
```

```bash
npm run dev
# GET http://localhost:3000 → "Olá, mundo!"
```

## Anatomia da rota

```typescript
app.get("/caminho", (req, res) => {
  // 1        2         3    4
});
```

1. **Método** — `get`, `post`, `patch`, `delete`
2. **Caminho** — `/`, `/usuarios`, `/produtos/:id`
3. **`req`** — tudo que chega (params, query, body, headers)
4. **`res`** — tudo que sai (`send`, `json`, `status`)

## `res.send` vs `res.json`

```typescript
res.send("texto");                  // Content-Type: text/html
res.send({ nome: "Ana" });          // converte pra JSON automaticamente
res.json({ nome: "Ana" });          // explícito — prefira para API
res.status(201).json({ id: 1 });    // encadeia status + corpo
```

`res.json()` é o padrão de API — deixa o contrato claro.

## Respondendo diferentes formatos

```typescript
app.get("/texto", (req, res) => res.send("Olá"));
app.get("/json", (req, res) => res.json({ ok: true }));
app.get("/vazio", (req, res) => res.status(204).send());
app.get("/html", (req, res) => res.send("<h1>Olá</h1>"));
```

## Testando

```bash
# curl
curl http://localhost:3000/json

# Thunder Client / Insomnia / Postman
# ou no browser para GETs
```

## O callback do listen

```typescript
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor na porta ${PORT}`);
});
```

Só roda quando o servidor sobe — bom lugar para logar a URL.

## Resumo

- `app.get(path, handler)` — método + caminho + função `(req, res)`
- `res.json()` para API; `res.status()` encadeia antes
- `app.listen(PORT)` sobe o servidor; callback confirma
- Teste com curl ou Thunder Client
