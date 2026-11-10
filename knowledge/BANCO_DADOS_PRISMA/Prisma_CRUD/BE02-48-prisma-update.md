# BE02-48 — Prisma: Update

## O básico

```ts
const usuario = await prisma.usuario.update({
  where: { id: 1 },
  data: { nome: "Ana Silva" },
});
// retorna o objeto ATUALIZADO
```

`where` precisa de campo único (`@id`/`@unique`) — update é sempre em um registro identificado.

## Campos parciais — o PATCH natural

```ts
await prisma.usuario.update({
  where: { id: 1 },
  data: { telefone: "9999-0000" },
});
// só telefone muda — os demais campos ficam como estão
```

`undefined` no `data` = "não alterar":

```ts
data: { nome: dados.nome }          // se nome for undefined, campo preservado
```

Isso faz do `update` um PATCH natural — envie só o que mudou.

## Operações atômicas em número

```ts
await prisma.produto.update({
  where: { id: 7 },
  data: { estoque: { decrement: 1 } },
});
```

| Operação | SQL gerado |
| --- | --- |
| `increment: n` | `estoque = estoque + n` |
| `decrement: n` | `estoque = estoque - n` |
| `multiply: n` | `estoque = estoque * n` |
| `divide: n` | `estoque = estoque / n` |
| `set: n` | `estoque = n` |

Atômico = duas requisições simultâneas não se pisam — o decremento acontece no banco, não na aplicação.

## Update em relação

```ts
// trocar o autor do livro
await prisma.livro.update({
  where: { id: 1 },
  data: { autor: { connect: { id: 2 } } },
});

// desligar (FK nullable)
await prisma.livro.update({
  where: { id: 1 },
  data: { autor: { disconnect: true } },
});
```

## update com select

```ts
await prisma.usuario.update({
  where: { id: 1 },
  data: { senha: novoHash },
  select: { id: true, email: true },   // não devolve o hash
});
```

## upsert — create OU update

```ts
await prisma.usuario.upsert({
  where: { email: "ana@mail.com" },
  create: { nome: "Ana", email: "ana@mail.com" },
  update: { nome: "Ana Silva" },
});
```

Existe → atualiza; não existe → cria. Útil para seeds e sincronizações.

## updateOrThrow? Não existe — P2025

```ts
await prisma.usuario.update({
  where: { id: 999 },          // não existe
  data: { nome: "X" },
});
// P2025: Record to update not found → mapear para 404
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `P2025` — update em id inexistente | Trate como 404 ou cheque com findUnique antes |
| Update em massa com `update` | `update` é por id — use `updateMany` para vários |
| Ler-e-escrever separado | `estoque - 1` lido + salvo tem race — use `decrement` |
| `null` vs `undefined` | `undefined` ignora; `null` grava NULL de verdade |

## Resumo

- `update({ where: único, data })` — retorna o objeto atualizado
- `undefined` pula o campo → PATCH natural
- `increment`/`decrement`/`multiply`/`divide` são atômicos no banco
- `connect`/`disconnect` mexem em relações; `upsert` = create-or-update
- P2025 → 404
