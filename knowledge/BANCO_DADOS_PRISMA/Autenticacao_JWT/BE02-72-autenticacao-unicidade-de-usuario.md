# BE02-72 — Autenticação: Unicidade de Usuário

## O problema

Dois cadastros com o mesmo email = dois usuários, um login. O email precisa ser único — e a verificação tem duas camadas.

## Camada 1 — banco (a garantia real)

```prisma
model Usuario {
  id    Int    @id @default(autoincrement())
  email String @unique     // ← UNIQUE no Postgres
}
```

A constraint `@unique` é a **única garantia verdadeira** — mesmo que a aplicação falhe, o banco impede duplicata.

## Camada 2 — aplicação (o erro amigável)

```ts
export async function registrar(dados: RegisterDto) {
  const existe = await prisma.usuario.findUnique({
    where: { email: dados.email },
  });
  if (existe) throw new AppError("Email já cadastrado", 409);

  return prisma.usuario.create({
    data: { ...dados, senha: await bcrypt.hash(dados.senha, 10) },
  });
}
```

Check antes → 409 semântico em vez de `P2002` genérico estourando 500.

## A race condition

```text
req A: findUnique(email) → não existe
req B: findUnique(email) → não existe     (mesmo instante)
req A: create → ok
req B: create → P2002!
```

O check não elimina a janela — a constraint sim. Então trate o `P2002` também:

```ts
import { Prisma } from "@prisma/client";

try {
  return await prisma.usuario.create({ ... });
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === "P2002") {
    throw new AppError("Email já cadastrado", 409);
  }
  throw e;
}
```

Check = UX boa na maioria; constraint + catch = correção em todos.

## Mapeando P2002 no middleware de erro

```ts
// middlewares/error.middleware.ts
export function handleErrors(err, req, res, next) {
  if (err instanceof Prisma.PrismaClientKnownRequestError) {
    if (err.code === "P2002") {
      const campo = (err.meta?.target as string[])?.join(", ");
      return res.status(409).json({ message: `${campo} já está em uso` });
    }
  }
  // ...
}
```

`err.meta.target` diz **qual** campo violou — `email` em `["email"]`.

## Status codes de unicidade

| Situação | Status |
| --- | --- |
| Cadastro ok | `201` |
| Email duplicado | `409` Conflict |
| Body malformado | `400` |
| Sem token em rota auth | `401` |

`409` é o semântico correto para unicidade — recurso já existe.

## Unicidade em outros contextos

```ts
// PATCH — atualizar para um email que outro usa
await prisma.usuario.update({
  where: { id: 2 },
  data: { email: "de-outro@mail.com" },
});
// P2002 também — update viola UNIQUE igual
```

```ts
// junção — matrícula dupla
await prisma.matricula.create({ data: { estudanteId: 1, cursoId: 2 } });
// P2002 na @@unique([estudanteId, cursoId]) → 409 "já matriculado"
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Só check, sem constraint | Race deixa duplicar — `@unique` no schema |
| P2002 virando 500 | Trate no service ou middleware → 409 |
| `400` para duplicata | `409` é o semântico — conflito de estado |
| Checkar `findFirst` com email case | Decida: `mode: "insensitive"` ou normalize lowercase |

## Resumo

- `@unique` no schema é a garantia real; check prévio é a UX
- Race condition existe entre check e insert — sempre trate `P2002`
- `P2002` → `409`; `meta.target` identifica o campo
- Unicidade vale também em update e em junções (`@@unique`)
