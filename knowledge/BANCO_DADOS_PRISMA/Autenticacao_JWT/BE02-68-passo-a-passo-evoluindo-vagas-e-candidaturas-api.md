# BE02-68 — Passo a Passo: Evoluindo Vagas e Candidaturas API

## O que muda

A API de BE02-56 ganha autenticação: cadastro com hash, login com JWT, rotas protegidas.

```text
Antes:                       Agora:
POST /candidatos (aberto)    POST /auth/register  → bcrypt
POST /vagas (aberto)         POST /auth/login     → JWT
                             rotas de vaga/candidatura → authMiddleware
```

## Ajustes no schema

```prisma
model Candidato {
  id           Int           @id @default(autoincrement())
  nome         String
  email        String        @unique
  senha        String        // ← hash bcrypt agora
  candidaturas Candidatura[]

  @@map("candidatos")
}
```

```bash
npx prisma migrate dev --name add_senha_candidato
```

## Service de autenticação

```ts
export async function registrar(dados: { nome: string; email: string; senha: string }) {
  const existe = await prisma.candidato.findUnique({
    where: { email: dados.email },
  });
  if (existe) throw new AppError("Email já cadastrado", 409);

  return prisma.candidato.create({
    data: { ...dados, senha: await bcrypt.hash(dados.senha, 10) },
    select: { id: true, nome: true, email: true },   // sem senha no retorno
  });
}

export async function login(email: string, senha: string) {
  const candidato = await prisma.candidato.findUnique({ where: { email } });
  const confere = candidato && await bcrypt.compare(senha, candidato.senha);
  if (!confere) throw new AppError("Credenciais inválidas", 401);

  const token = jwt.sign({}, process.env.JWT_SECRET as string, {
    subject: candidato.id.toString(),
    expiresIn: "1d",
  });
  return { accessToken: token };
}
```

## Rotas públicas vs protegidas

```ts
// públicas
router.post("/auth/register", controller.registrar);
router.post("/auth/login", controller.login);
router.get("/vagas", controller.listarVagas);       // catálogo aberto

// protegidas
router.post("/vagas", authMiddleware, controller.criarVaga);
router.post("/vagas/:id/candidaturas", authMiddleware, controller.candidatar);
router.get("/minhas-candidaturas", authMiddleware, controller.minhas);
```

## Regra de negócio com identidade

```ts
export async function candidatar(candidatoId: number, vagaId: number) {
  // candidatoId vem do token — é "você", não arbitrário
  const vaga = await prisma.vaga.findUnique({ where: { id: vagaId } });
  if (!vaga) throw new AppError("Vaga não encontrada", 404);

  const ja = await prisma.candidatura.findUnique({
    where: { candidatoId_vagaId: { candidatoId, vagaId } },
  });
  if (ja) throw new AppError("Já candidatado", 409);

  return prisma.candidatura.create({
    data: { candidatoId, vagaId },
  });
}
```

```ts
// rota usa o id do token
router.post("/vagas/:id/candidaturas", authMiddleware, async (req, res) => {
  const c = await candidatar(res.locals.usuarioId, Number(req.params.id));
  return res.status(201).json(c);
});
```

## Endpoints finais

```text
POST   /auth/register            → 201 (sem senha no retorno)
POST   /auth/login               → { accessToken }
GET    /vagas                    → público
POST   /vagas                    → auth (empresa/recrutador)
POST   /vagas/:id/candidaturas   → auth, candidatoId do token
GET    /minhas-candidaturas      → auth, where: { candidatoId: token }
PATCH  /candidaturas/:id         → auth + dono
DELETE /candidatos/me            → auth + cascade
```

## O que a aula consolida

1. bcrypt no register, `select` sem `senha`
1. Erro genérico no login — sem enumeração
1. `authMiddleware` antes do handler
1. Identidade do token — body não decide "quem"
1. `@@unique` composta + 409 = "já candidatado"

## Resumo

- Autenticação entra como camada: register/login públicos, resto atrás do middleware
- `res.locals.usuarioId` é a fonte de "quem sou eu" nas regras
- Login 401 genérico, duplicata 409, dono errado 403
- A API inteira agora conhece o usuário — a base das entregas finais
