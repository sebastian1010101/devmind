# BE01-44 — Atividade: Praticando Arquitetura

Exercício: estruturar uma API em camadas — routes → controllers → services → database.

## Estrutura de pastas

```text
src/
├── app.ts
├── server.ts
├── database/
│   └── produtos.database.ts      → array + operações
├── interfaces/
│   └── produto.interface.ts      → Produto, DTOs, IProdutoRepository
├── services/
│   └── produto.service.ts        → regras de negócio
├── controllers/
│   └── produto.controller.ts     → HTTP ↔ service
└── routes/
    └── produto.routes.ts         → endpoints
```

## interfaces/produto.interface.ts

```typescript
export interface Produto {
  id: number;
  nome: string;
  preco: number;
}

export type CriarProdutoDTO = Omit<Produto, "id">;
export type AtualizarProdutoDTO = Partial<CriarProdutoDTO>;
```

## database/produtos.database.ts

```typescript
import { Produto } from "../interfaces/produto.interface";

export const produtos: Produto[] = [];
export let proximoId = 1;
export const incrementarId = () => proximoId++;
```

## services/produto.service.ts

```typescript
import { produtos, incrementarId } from "../database/produtos.database";
import { CriarProdutoDTO, Produto } from "../interfaces/produto.interface";

export class ProdutoService {
  listar(): Produto[] {
    return produtos;
  }

  buscar(id: number): Produto | undefined {
    return produtos.find((p) => p.id === id);
  }

  criar(dados: CriarProdutoDTO): Produto {
    const produto: Produto = { id: incrementarId(), ...dados };
    produtos.push(produto);
    return produto;
  }
}
```

## controllers/produto.controller.ts

```typescript
import { Request, Response } from "express";
import { ProdutoService } from "../services/produto.service";

export class ProdutoController {
  constructor(private service: ProdutoService) {}

  listar = (req: Request, res: Response) => {
    return res.json(this.service.listar());
  };

  buscar = (req: Request, res: Response) => {
    const produto = this.service.buscar(Number(req.params.id));
    if (!produto) {
      return res.status(404).json({ message: "Não encontrado" });
    }
    return res.json(produto);
  };

  criar = (req: Request, res: Response) => {
    return res.status(201).json(this.service.criar(req.body));
  };
}
```

> Arrow function no método: `this` fica ligado à instância — essencial quando o método é passado como callback para a rota.

## routes/produto.routes.ts

```typescript
import { Router } from "express";
import { ProdutoController } from "../controllers/produto.controller";
import { ProdutoService } from "../services/produto.service";

const service = new ProdutoService();
const controller = new ProdutoController(service);

const router = Router();
router.get("/", controller.listar);
router.get("/:id", controller.buscar);
router.post("/", controller.criar);

export default router;
```

## Checklist

- [ ] Service não toca em `req`/`res`
- [ ] Controller não tem lógica de negócio
- [ ] Métodos do controller são arrow functions (binding do `this`)
- [ ] Injeção: `new ProdutoController(service)` no routes
- [ ] Interfaces em arquivo próprio

## Resumo

- 4 pastas = 4 responsabilidades: database, services, controllers, routes
- Arrow methods no controller preservam `this` como callback
- Injeção manual no routes — base para DI de verdade (NestJS)
