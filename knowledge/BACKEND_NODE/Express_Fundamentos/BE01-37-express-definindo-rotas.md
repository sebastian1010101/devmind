# BE01-37 — Express: Definindo Rotas

## Os métodos de rota

```typescript
app.get("/produtos", listar);
app.post("/produtos", criar);
app.get("/produtos/:id", buscar);
app.patch("/produtos/:id", atualizar);
app.delete("/produtos/:id", remover);
```

## Parâmetros de rota

```typescript
app.get("/produtos/:id", (req, res) => {
  const id = Number(req.params.id);   // params são SEMPRE strings
  res.json({ id });
});

// Múltiplos
app.get("/usuarios/:userId/pedidos/:pedidoId", (req, res) => {
  res.json(req.params); // { userId: "3", pedidoId: "7" }
});
```

## Query string

```typescript
// GET /produtos?categoria=eletronicos&pagina=2
app.get("/produtos", (req, res) => {
  const { categoria, pagina } = req.query; // tudo string
  res.json({ categoria, pagina: Number(pagina) || 1 });
});
```

## Handlers nomeados vs inline

```typescript
// Inline — rápido, mas o arquivo cresce
app.get("/produtos", (req, res) => { /* ... */ });

// Nomeado — prepara para controllers (BE01-43)
const listar = (req: Request, res: Response) => { /* ... */ };
app.get("/produtos", listar);
```

## Tipando o handler

```typescript
import { Request, Response } from "express";

const buscar = (req: Request<{ id: string }>, res: Response) => {
  req.params.id; // tipado como string
};
```

## Ordem importa

```typescript
app.get("/produtos/novo", handler);  // ✅ antes do :id
app.get("/produtos/:id", handler);   // captura "novo" como id se vier antes
```

Rotas específicas antes de rotas com parâmetro.

## `app.all` e fallback

```typescript
// Qualquer método
app.all("/ping", (req, res) => res.json({ pong: true }));

// 404 para rotas não encontradas — por último
app.use((req, res) => {
  res.status(404).json({ message: "Rota não encontrada" });
});
```

## Resumo

- `app.{verbo}(path, handler)`; `:param` vira `req.params`
- Params e query são strings — converta
- Handlers nomeados preparam a arquitetura em camadas
- Rotas específicas antes de `:param`; fallback 404 por último
