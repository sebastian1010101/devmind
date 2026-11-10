# BE01-49 — Errors: Classe Customizada

## O problema com Error genérico

```typescript
throw new Error("Usuário não encontrado");
```

O handler de erro recebe uma mensagem — mas qual status HTTP usar? `Error` nativo não carrega `statusCode`.

## AppError — erro de domínio

```typescript
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 400
  ) {
    super(message);
    this.name = "AppError";
  }
}
```

```typescript
throw new AppError("Usuário não encontrado", 404);
throw new AppError("Email já cadastrado", 409);
throw new AppError("Saldo insuficiente", 422);
```

O erro viaja **com** seu status HTTP — o middleware de erro só lê `err.statusCode`.

## Por que `extends Error`

- `instanceof Error` continua funcionando
- `err.stack`, `err.message` herdados de graça
- Middleware distingue `AppError` (esperado) de erro inesperado (bug)

## Hierarquia de erros

```typescript
class AppError extends Error {
  constructor(message: string, public statusCode = 400) {
    super(message);
  }
}

class NotFoundError extends AppError {
  constructor(recurso: string) {
    super(`${recurso} não encontrado`, 404);
  }
}

class ConflictError extends AppError {
  constructor(msg: string) {
    super(msg, 409);
  }
}

class UnauthorizedError extends AppError {
  constructor(msg = "Não autorizado") {
    super(msg, 401);
  }
}
```

```typescript
// service — semântico e limpo
throw new NotFoundError("Produto");
throw new ConflictError("Email já em uso");
```

## No service vs no middleware

```typescript
// Service lança — não sabe de HTTP além do statusCode
criar(dados: CriarDTO) {
  if (this.repo.buscarPorEmail(dados.email)) {
    throw new ConflictError("Email já cadastrado");
  }
  return this.repo.criar(dados);
}
```

```typescript
// Controller não trata — deixa estourar pro middleware de erro
criar = (req: Request, res: Response) => {
  const usuario = this.service.criar(req.body); // se lançar, middleware pega
  return res.status(201).json(usuario);
};
```

## Com async handlers

```typescript
// Express 4: async precisa de next(e) — ou o erro não chega ao middleware
criar = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const u = await this.service.criar(req.body);
    return res.status(201).json(u);
  } catch (e) {
    next(e);
  }
};
```

Express 5 captura erros de promise automaticamente; no 4, `next(e)` ou um wrapper.

## O que não vira AppError

Bug do programador (`undefined.map`, typo) → `Error` nativo → `500` genérico. `AppError` é para **casos esperados** do domínio.

## Resumo

- `AppError extends Error` carrega `statusCode` — erro viaja completo
- Subclasses semânticas: `NotFoundError`, `ConflictError`, `UnauthorizedError`
- Service lança; middleware de erro traduz pra HTTP
- AppError = esperado; Error nativo = bug → 500
