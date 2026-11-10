# BE02-65 — Utilizando JWT — Parte 3

## O fluxo de login completo

```text
POST /login
  { email, senha }
      ↓
  1. findUnique por email          → não achou? 401
  2. bcrypt.compare(senha, hash)   → não confere? 401
  3. jwt.sign({ sub: id })         → devolve token
```

## A rota de login

```ts
// services/auth.service.ts
export async function login(email: string, senha: string) {
  const usuario = await prisma.usuario.findUnique({ where: { email } });
  if (!usuario) {
    throw new AppError("Credenciais inválidas", 401);   // não diga qual errou
  }

  const confere = await bcrypt.compare(senha, usuario.senha);
  if (!confere) {
    throw new AppError("Credenciais inválidas", 401);
  }

  const token = jwt.sign(
    { email: usuario.email },
    process.env.JWT_SECRET as string,
    { subject: usuario.id.toString(), expiresIn: "1d" }
  );

  return { accessToken: token };
}
```

```ts
router.post("/login", async (req, res) => {
  const { accessToken } = await login(req.body.email, req.body.senha);
  return res.json({ accessToken });
});
```

## Por que "Credenciais inválidas" genérico

```text
❌ "email não encontrado"  → confirmou que o email existe (enumeração)
❌ "senha errada"          → confirmou que o email existe
✅ "credenciais inválidas" → não entrega informação
```

Mesmo status `401` para os dois casos — não vaze se o email existe.

## Registro → hash → login

```ts
// register
const hash = await bcrypt.hash(senha, 10);
await prisma.usuario.create({
  data: { nome, email, senha: hash },
});

// login
const confere = await bcrypt.compare(senhaDigitada, usuario.senha);
```

`hash` é unidirecional — a senha nunca é descriptografada, só comparada.

## Rota protegida completa

```ts
// middleware de auth + service usando o usuarioId
router.post("/vagas", authMiddleware, async (req, res) => {
  const vaga = await criarVaga(req.body, res.locals.usuarioId);
  return res.status(201).json(vaga);
});
```

```ts
export async function criarVaga(dados: CreateVaga, donoId: number) {
  return prisma.vaga.create({
    data: { ...dados, empresaId: donoId },   // dono vem do token, não do body
  });
}
```

**O id do usuário vem do token** — nunca confie em `req.body.usuarioId` (qualquer um forja).

## Recursos do próprio usuário

```ts
// GET /me — "eu"
router.get("/me", authMiddleware, async (req, res) => {
  const usuario = await prisma.usuario.findUniqueOrThrow({
    where: { id: res.locals.usuarioId },
  });
  return res.json(usuario);
});

// PATCH /usuarios/:id — só o próprio
router.patch("/usuarios/:id", authMiddleware, async (req, res) => {
  if (Number(req.params.id) !== res.locals.usuarioId) {
    return res.status(403).json({ message: "Acesso negado" });
  }
  // ...
});
```

`401` = não autenticado; `403` = autenticado mas sem permissão.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Aceitar `usuarioId` do body | Dono vem do token — body é forjável |
| Mensagem diferente por email/senha | Uniforme: "credenciais inválidas" |
| Comparar senha com `===` | `bcrypt.compare` — senha é hash |
| 401 e 403 invertidos | 401 sem token; 403 sem permissão |

## Resumo

- Login = findUnique → bcrypt.compare → jwt.sign
- Erro genérico "credenciais inválidas" — não enumere usuários
- Identidade real vem do `token`/`res.locals` — nunca do body
- `401` não logado, `403` sem permissão
