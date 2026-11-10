# BE01-41 — Express: Router

## O problema

Todas as rotas num `index.ts` só não escala:

```text
index.ts com 30 rotas → arquivo gigante, responsabilidades misturadas
```

## `express.Router()` — módulo de rotas

```typescript
// src/routes/produtos.routes.ts
import { Router } from "express";

const produtosRouter = Router();

produtosRouter.get("/", listar);        // vira GET /produtos
produtosRouter.get("/:id", buscar);     // vira GET /produtos/:id
produtosRouter.post("/", criar);        // vira POST /produtos
produtosRouter.patch("/:id", atualizar);
produtosRouter.delete("/:id", remover);

export default produtosRouter;
```

```typescript
// src/app.ts
import produtosRouter from "./routes/produtos.routes";

app.use("/produtos", produtosRouter);  // prefixo — as rotas dentro são relativas
```

## Estrutura resultante

```text
src/
├── app.ts                      → cria app, monta routers, middlewares globais
├── server.ts                   → app.listen (separado da app — BE01-51)
└── routes/
    ├── produtos.routes.ts      → Router() com rotas relativas "/"
    ├── usuarios.routes.ts
    └── pedidos.routes.ts
```

## Router com middleware local

Middlewares podem valer só para um router:

```typescript
const adminRouter = Router();

adminRouter.use(verificaAdmin);  // só rotas de admin passam por ele

adminRouter.get("/usuarios", listarUsuarios);
adminRouter.delete("/usuarios/:id", removerUsuario);
```

## Router aninhado

```typescript
// /pedidos/:pedidoId/itens
const itensRouter = Router({ mergeParams: true });
// mergeParams: acessa :pedidoId do router pai

itensRouter.get("/", (req, res) => {
  req.params.pedidoId; // disponível graças ao mergeParams
});
```

## app.js vs routes

```typescript
// app.ts — composição, sem lógica de negócio
import express from "express";
import produtosRouter from "./routes/produtos.routes";
import usuariosRouter from "./routes/usuarios.routes";

const app = express();
app.use(express.json());
app.use("/produtos", produtosRouter);
app.use("/usuarios", usuariosRouter);

export default app;
```

## Resumo

- `Router()` agrupa rotas; `app.use("/prefixo", router)` monta
- Rotas dentro do router são relativas ao prefixo
- `router.use(middleware)` aplica só naquele grupo
- `mergeParams` para routers aninhados verem params do pai
