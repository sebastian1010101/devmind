# BE02-64 — Utilizando JWT — Parte 2

## verify — validando o token

```ts
import jwt from "jsonwebtoken";

try {
  const payload = jwt.verify(token, process.env.JWT_SECRET as string);
  // payload → { sub: "42", email: "...", iat, exp }
} catch (e) {
  // token inválido, expirado ou adulterado
}
```

`verify` checa assinatura **e** `exp` — lança erro em ambos os casos.

## Os erros do verify

| Erro | Significa |
| --- | --- |
| `TokenExpiredError` | Passou do `exp` |
| `JsonWebTokenError` | Assinatura inválida, malformado |
| `NotBeforeError` | `nbf` ainda não alcançado |

```ts
catch (e) {
  if (e instanceof jwt.TokenExpiredError) {
    return res.status(401).json({ message: "Token expirado" });
  }
  return res.status(401).json({ message: "Token inválido" });
}
```

## O middleware de autenticação

```ts
// middlewares/auth.middleware.ts
import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const { authorization } = req.headers;

  if (!authorization) {
    return res.status(401).json({ message: "Token não fornecido" });
  }

  const [, token] = authorization.split(" ");   // "Bearer <token>"

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET as string);

    if (typeof payload === "string" || !payload.sub) {
      return res.status(401).json({ message: "Token inválido" });
    }

    res.locals.usuarioId = Number(payload.sub);   // disponível na rota
    return next();
  } catch {
    return res.status(401).json({ message: "Token inválido" });
  }
}
```

`payload.sub` pode vir `undefined` — um token assinado sem `subject` (por exemplo, um refresh token customizado) passaria pelo `verify` mas `Number(undefined)` vira `NaN` silenciosamente. Sem essa checagem, `prisma.usuario.findUnique({ where: { id: NaN } })` simplesmente retorna `null` — um bug difícil de rastrear porque não há erro, só um 404 inesperado.

```text
Authorization: Bearer eyJhbGciOi...
                    ↑
            split(" ") pega a segunda parte
```

## res.locals — carregando o usuário

`res.locals` é o objeto por-requisição do Express — o middleware grava, a rota lê:

```ts
router.get("/me", authMiddleware, async (req, res) => {
  const usuario = await prisma.usuario.findUnique({
    where: { id: res.locals.usuarioId },
    select: { id: true, nome: true, email: true },
  });
  return res.json(usuario);
});
```

Alternativa tipada — estender `Request` com declaration merging ou passar via `res.locals` com interface.

## Aplicando nas rotas

```ts
// rota a rota
router.get("/vagas", authMiddleware, controller.listar);

// grupo inteiro
router.use("/admin", authMiddleware, adminRoutes);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `Bearer undefined` | Cliente não mandou header — ou header com typo |
| Token no body em vez de header | O padrão é `Authorization: Bearer` |
| `verify` com segredo errado | Mesma `JWT_SECRET` do `sign` — confira o `.env` |
| `req.user` sem tipagem | Use `res.locals` ou estenda o tipo `Request` |
| Esquecer `return` no erro | `return res.status(401)...` — senão roda o resto |

## Resumo

- `jwt.verify(token, secret)` valida assinatura + expiração — lança erro
- Middleware extrai `Bearer`, verifica, grava `res.locals.usuarioId`
- `next()` segue; sem token → `401` com `return` (interrompe)
- Rota protegida = `router.get(x, authMiddleware, handler)`
