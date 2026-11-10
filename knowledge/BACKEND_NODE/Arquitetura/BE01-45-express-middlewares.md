# BE01-45 — Express: Middlewares

## O que é

Uma função que fica **entre** a requisição e a resposta — pode inspecionar, modificar, bloquear ou deixar passar:

```text
Request → [Middleware 1] → [Middleware 2] → [Handler] → Response
              │                  │
              └── bloqueia? → res direto (sem chamar o handler)
```

## Anatomia

```typescript
const middleware = (req: Request, res: Response, next: NextFunction) => {
  // 1. fazer algo com req
  // 2. decidir:
  next();                           // → deixa passar pro próximo
  // ou
  res.status(401).json({ ... });    // → encerra aqui (sem next)
};
```

`next()` = "passe adiante". Sem `next()` e sem `res.*` = request pendurado para sempre.

## Onde se registram

```typescript
// Global — toda request passa
app.use(meuMiddleware);

// Em uma rota
app.get("/admin", verificaAdmin, handler);

// Num router inteiro
adminRouter.use(verificaAdmin);

// Vários em sequência
app.post("/produtos", validaBody, verificaAuth, handler);
```

## Exemplos clássicos

### Logger

```typescript
const logger = (req: Request, res: Response, next: NextFunction) => {
  console.log(`${req.method} ${req.path} — ${new Date().toISOString()}`);
  next();
};
```

### Autenticação

```typescript
const autenticado = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).json({ message: "Token ausente" });
  }
  // valida token...
  next();
};
```

### Anexando dados ao request

```typescript
const identifica = (req: Request, res: Response, next: NextFunction) => {
  res.locals.usuarioId = extrairDoToken(req); // locals: bagagem do request
  next();
};
```

`res.locals` é o jeito idiomático de passar dados entre middlewares — sobrevive só durante aquela request.

## Middleware de erro — 4 parâmetros

```typescript
// O Express reconhece como error-handler pelos 4 parâmetros
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  res.status(500).json({ message: err.message });
});
```

Registrado **depois de todas as rotas** — captura o que ninguém tratou (BE01-50 detalha).

## Ordem = comportamento

```typescript
app.use(express.json());     // 1. parseia body
app.use(logger);             // 2. loga
app.use("/api", router);     // 3. rotas
app.use(errorHandler);       // 4. erros — por último
```

Middleware registrado depois da rota **não roda** para ela — a resposta já foi enviada.

## Middlewares prontos do ecossistema

```typescript
import cors from "cors";
import helmet from "helmet";

app.use(cors());             // libera CORS
app.use(helmet());           // headers de segurança (BE01-54)
app.use(express.json());     // nativo
```

## Resumo

- Middleware = `(req, res, next)` — inspeciona, modifica, bloqueia ou `next()`
- Global (`app.use`), por rota ou por router
- `res.locals` passa dados entre middlewares da mesma request
- Ordem importa; error-handler tem 4 parâmetros e vai por último
