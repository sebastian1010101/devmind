# BE01-52 — Passo a Passo: Cars API

Consolidação completa: API REST de carros com todas as camadas.

## Estrutura

```text
src/
├── app.ts
├── server.ts
├── database/cars.database.ts
├── interfaces/car.interface.ts
├── errors/AppError.ts
├── services/car.service.ts
├── controllers/car.controller.ts
├── routes/car.routes.ts
└── middlewares/
    ├── validateId.middleware.ts
    └── handleErrors.middleware.ts
```

## interface + database

```typescript
export interface Car {
  id: number;
  modelo: string;
  marca: string;
  ano: number;
  preco: number;
}

export type CreateCarDTO = Omit<Car, "id">;
export type UpdateCarDTO = Partial<CreateCarDTO>;
```

```typescript
export const cars: Car[] = [];
let nextId = 1;
export const getNextId = () => nextId++;
```

## service — regras

```typescript
export class CarService {
  listar(): Car[] {
    return cars;
  }

  buscar(id: number): Car {
    const car = cars.find((c) => c.id === id);
    if (!car) throw new AppError("Carro não encontrado", 404);
    return car;
  }

  criar(dados: CreateCarDTO): Car {
    if (dados.ano < 1886) throw new AppError("Ano inválido");
    const car: Car = { id: getNextId(), ...dados };
    cars.push(car);
    return car;
  }

  atualizar(id: number, dados: UpdateCarDTO): Car {
    const car = this.buscar(id);
    Object.assign(car, dados);
    return car;
  }

  remover(id: number): void {
    const car = this.buscar(id);
    cars.splice(cars.indexOf(car), 1);
  }
}
```

## controller — HTTP

```typescript
export class CarController {
  constructor(private service: CarService) {}

  listar = (req: Request, res: Response) => res.json(this.service.listar());

  buscar = (req: Request, res: Response) =>
    res.json(this.service.buscar(Number(req.params.id)));

  criar = (req: Request, res: Response) =>
    res.status(201).json(this.service.criar(req.body));

  atualizar = (req: Request, res: Response) =>
    res.json(this.service.atualizar(Number(req.params.id), req.body));

  remover = (req: Request, res: Response) => {
    this.service.remover(Number(req.params.id));
    return res.status(204).send();
  };
}
```

## middleware de validação de id

```typescript
export const validateId = (req: Request, res: Response, next: NextFunction) => {
  const id = Number(req.params.id);
  if (isNaN(id) || id <= 0) {
    return res.status(400).json({ message: "ID inválido" });
  }
  next();
};
```

## routes

```typescript
const service = new CarService();
const controller = new CarController(service);

const carRouter = Router();
carRouter.get("/", controller.listar);
carRouter.get("/:id", validateId, controller.buscar);
carRouter.post("/", controller.criar);
carRouter.patch("/:id", validateId, controller.atualizar);
carRouter.delete("/:id", validateId, controller.remover);
```

## app.ts + server.ts

```typescript
const app = express();
app.use(express.json());
app.use("/cars", carRouter);
app.use(handleErrors); // por último
export default app;
```

## Checklist da consolidação

- [ ] 5 endpoints REST funcionando
- [ ] `validateId` antes dos handlers com `:id`
- [ ] Service lança `AppError`; middleware traduz pra HTTP
- [ ] Controller sem `if` de negócio
- [ ] `app`/`server` separados

## Resumo

- Pipeline completo: route → middleware → controller → service → database
- `AppError` conecta domínio e HTTP via `handleErrors`
- Estrutura pronta para trocar array por Prisma (módulo 07)
