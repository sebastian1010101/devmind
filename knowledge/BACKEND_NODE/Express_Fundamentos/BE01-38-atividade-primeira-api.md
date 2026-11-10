# BE01-38 — Atividade: Minha Primeira API

Exercício: primeira API completa em memória — CRUD de tarefas.

## Setup

```bash
npm init -y
npm install express
npm install -D typescript @types/node @types/express ts-node-dev
npx tsc --init
```

## Implementação

```typescript
import express, { Request, Response } from "express";

interface Tarefa {
  id: number;
  titulo: string;
  concluida: boolean;
}

const app = express();
app.use(express.json());

const tarefas: Tarefa[] = [];
let proximoId = 1;

// Listar
app.get("/tarefas", (req: Request, res: Response) => {
  res.json(tarefas);
});

// Buscar uma
app.get("/tarefas/:id", (req, res) => {
  const tarefa = tarefas.find((t) => t.id === Number(req.params.id));
  if (!tarefa) {
    return res.status(404).json({ message: "Tarefa não encontrada" });
  }
  res.json(tarefa);
});

// Criar
app.post("/tarefas", (req, res) => {
  const { titulo } = req.body;
  if (!titulo || typeof titulo !== "string") {
    return res.status(400).json({ message: "Título é obrigatório" });
  }
  const tarefa: Tarefa = { id: proximoId++, titulo, concluida: false };
  tarefas.push(tarefa);
  res.status(201).json(tarefa);
});

// Atualizar
app.patch("/tarefas/:id", (req, res) => {
  const tarefa = tarefas.find((t) => t.id === Number(req.params.id));
  if (!tarefa) {
    return res.status(404).json({ message: "Tarefa não encontrada" });
  }
  const { titulo, concluida } = req.body;
  if (titulo !== undefined) tarefa.titulo = titulo;
  if (concluida !== undefined) tarefa.concluida = concluida;
  res.json(tarefa);
});

// Remover
app.delete("/tarefas/:id", (req, res) => {
  const indice = tarefas.findIndex((t) => t.id === Number(req.params.id));
  if (indice === -1) {
    return res.status(404).json({ message: "Tarefa não encontrada" });
  }
  tarefas.splice(indice, 1);
  res.status(204).send();
});

app.listen(3000, () => console.log("API em http://localhost:3000"));
```

## Testando

```bash
curl -X POST http://localhost:3000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Estudar Express"}'

curl http://localhost:3000/tarefas
curl -X PATCH http://localhost:3000/tarefas/1 -H "Content-Type: application/json" -d '{"concluida": true}'
curl -X DELETE http://localhost:3000/tarefas/1
```

## Checklist

- [ ] `express.json()` antes das rotas
- [ ] `201` no create, `204` no delete, `404` quando não existe
- [ ] `Number(req.params.id)` — params são strings
- [ ] Validação mínima do body (Zod vem em BE01-56)
- [ ] `return` antes de `res` nos early returns (encerra a função)

## Desafios

1. `GET /tarefas?concluida=true` — filtro por query
2. `DELETE /tarefas` — limpa só as concluídas
3. `GET /tarefas/stats` — `{ total, concluidas, pendentes }`

## Resumo

- 5 rotas cobrem o CRUD: GET lista/um, POST, PATCH, DELETE
- Status codes corretos: 201, 204, 404, 400
- Early return com `return res.status(404)...`
