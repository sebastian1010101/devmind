# BE01-42 — Atividade: Praticando Router

Exercício: refatorar a API de tarefas (BE01-38) separando rotas em routers.

## Estrutura

```text
src/
├── app.ts
├── server.ts
└── routes/
    ├── tarefas.routes.ts
    └── categorias.routes.ts
```

## routes/tarefas.routes.ts

```typescript
import { Router } from "express";

interface Tarefa {
  id: number;
  titulo: string;
  concluida: boolean;
}

const tarefasRouter = Router();
const tarefas: Tarefa[] = [];
let proximoId = 1;

tarefasRouter.get("/", (req, res) => res.json(tarefas));

tarefasRouter.post("/", (req, res) => {
  const tarefa: Tarefa = {
    id: proximoId++,
    titulo: req.body.titulo,
    concluida: false,
  };
  tarefas.push(tarefa);
  res.status(201).json(tarefa);
});

export default tarefasRouter;
```

## routes/categorias.routes.ts

```typescript
import { Router } from "express";

const categoriasRouter = Router();
const categorias = [
  { id: 1, nome: "Trabalho" },
  { id: 2, nome: "Pessoal" },
];

categoriasRouter.get("/", (req, res) => res.json(categorias));

export default categoriasRouter;
```

## app.ts e server.ts

```typescript
// app.ts
import express from "express";
import tarefasRouter from "./routes/tarefas.routes";
import categoriasRouter from "./routes/categorias.routes";

const app = express();
app.use(express.json());
app.use("/tarefas", tarefasRouter);
app.use("/categorias", categoriasRouter);

export default app;
```

```typescript
// server.ts
import app from "./app";

app.listen(3000, () => console.log("http://localhost:3000"));
```

Separar `app` de `server` permite importar o `app` em testes sem subir a porta.

## Testando

```bash
curl http://localhost:3000/tarefas
curl http://localhost:3000/categorias
```

## Checklist

- [ ] Cada recurso tem seu `.routes.ts` com `Router()`
- [ ] `app.use("/prefixo", router)` monta os módulos
- [ ] `app.ts` exporta app; `server.ts` faz o listen
- [ ] Zero lógica de rota no `app.ts`

## Desafios

1. Middleware `adminRouter.use(verificaToken)` só nas rotas de admin
2. Router aninhado `/categorias/:catId/tarefas` com `mergeParams`
3. Handler 404 global no `app.ts`

## Resumo

- Router separa recursos; app.ts só compõe
- app/server separados = app importável para testes
