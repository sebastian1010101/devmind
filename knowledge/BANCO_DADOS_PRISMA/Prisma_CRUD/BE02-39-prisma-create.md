# BE02-39 — Prisma: Create

## O básico

```ts
const usuario = await prisma.usuario.create({
  data: {
    nome: "Ana",
    email: "ana@mail.com",
  },
});
// retorna o objeto criado — com id e campos default preenchidos
```

É o equivalente a `INSERT ... RETURNING *`.

## O que `data` aceita

```ts
data: {
  nome: "Ana",                    // literal
  email: "ana@mail.com",
  idade: 28,
  ativo: true,
  perfil: { create: {...} },      // relação aninhada
}
```

Campos com `@default` (`id`, `criadoEm`) são omitidos — o banco preenche.

## Escolhendo o retorno — select

```ts
const usuario = await prisma.usuario.create({
  data: { nome: "Ana", email: "ana@mail.com", senha: hash },
  select: { id: true, nome: true, email: true },   // senha fica fora
});
```

`select` funciona em create também — ideal para não retornar `senha`/`hash`.

## Erros no create

```ts
import { Prisma } from "@prisma/client";

try {
  await prisma.usuario.create({ data: { nome: "Ana", email: "ana@mail.com" } });
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === "P2002") {
    // UNIQUE violada — email já existe
  }
  throw e;
}
```

| Código | Significa |
| --- | --- |
| `P2002` | Unique constraint violada |
| `P2003` | Foreign key inválida |
| `P2000` | Valor maior que a coluna |

## Em um service Express

```ts
async function criarUsuario(dados: CreateUsuarioDto) {
  const existe = await prisma.usuario.findUnique({
    where: { email: dados.email },
  });
  if (existe) throw new AppError("Email já cadastrado", 409);

  return prisma.usuario.create({
    data: { ...dados, senha: await hash(dados.senha, 10) },
    select: { id: true, nome: true, email: true },
  });
}
```

Verificar antes evita depender do `P2002` — mas o constraint no banco é a garantia real (race condition existe entre o check e o insert).

## Erros comuns

| Erro | Correção |
| --- | --- |
| Retornar senha/hash no response | `select` explícito — whitelist, não blacklist |
| `P2002` estourando 500 | Trate como 409 — ou valide antes |
| Passar `undefined` para campo | `undefined` = "não enviar" (diferente de `null`) |
| FK inexistente | `P2003` — o pai precisa existir ou use `connect` |

## Resumo

- `prisma.model.create({ data })` = INSERT + RETURNING
- `select` limita o retorno — nunca exponha hash de senha
- `P2002` = unique, `P2003` = FK — mapeie para 409/400 na API
- `undefined` omite o campo; `null` grava NULL
