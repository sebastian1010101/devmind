# BE02-69 — Atividade: Praticando Autenticação

## Objetivo

Implementar o ciclo completo: registro com bcrypt, login com JWT, rota protegida e regra de propriedade — numa API mínima de notas.

## Estrutura

```text
POST   /register        → cria usuário com hash
POST   /login           → devolve { accessToken }
GET    /notas           → auth — só as minhas notas
POST   /notas           → auth — dono = token
GET    /notas/:id       → auth — só se minha
DELETE /notas/:id       → auth — só se minha
```

## Schema mínimo

```prisma
model Usuario {
  id    Int    @id @default(autoincrement())
  email String @unique
  senha String
  notas Nota[]

  @@map("usuarios")
}

model Nota {
  id        Int     @id @default(autoincrement())
  texto     String
  usuario   Usuario @relation(fields: [usuarioId], references: [id], onDelete: Cascade)
  usuarioId Int     @map("usuario_id")

  @@map("notas")
}
```

## Services

```ts
export async function registrar(email: string, senha: string) {
  const hash = await bcrypt.hash(senha, 10);
  return prisma.usuario.create({
    data: { email, senha: hash },
    select: { id: true, email: true },
  });
}

export async function login(email: string, senha: string) {
  const u = await prisma.usuario.findUnique({ where: { email } });
  const ok = u && await bcrypt.compare(senha, u.senha);
  if (!ok) throw new AppError("Credenciais inválidas", 401);

  return { accessToken: jwt.sign({}, SECRET, { subject: String(u.id), expiresIn: "1h" }) };
}

export async function minhasNotas(usuarioId: number) {
  return prisma.nota.findMany({ where: { usuarioId } });
}

export async function criarNota(usuarioId: number, texto: string) {
  return prisma.nota.create({ data: { usuarioId, texto } });
}
```

## Regra de propriedade

```ts
export async function deletarNota(usuarioId: number, notaId: number) {
  const nota = await prisma.nota.findUnique({ where: { id: notaId } });

  if (!nota) throw new AppError("Nota não encontrada", 404);
  if (nota.usuarioId !== usuarioId) throw new AppError("Acesso negado", 403);

  await prisma.nota.delete({ where: { id: notaId } });
}
```

O filtro `usuarioId` no where também resolve — mas checar separado dá o `403` correto (existe, mas não é sua).

## Testes manuais

```bash
curl -X POST localhost:3000/register -d '{"email":"a@a.com","senha":"123"}' -H "Content-Type: application/json"
curl -X POST localhost:3000/login    -d '{"email":"a@a.com","senha":"123"}' -H "Content-Type: application/json"
curl localhost:3000/notas -H "Authorization: Bearer <token>"
curl localhost:3000/notas                              # → 401 sem token
```

## Critérios de conclusão

1. Senha gravada como hash — nunca em texto
1. Login errado → 401 genérico
1. `/notas` sem token → 401; com token → só as do usuário
1. Deletar nota de outro → 403

## Resumo

- Register/login/notas formam o ciclo auth completo
- Regra de propriedade: `usuarioId` do token vs do recurso → 403
- Todas as rotas de "meus dados" filtram pelo id do token
