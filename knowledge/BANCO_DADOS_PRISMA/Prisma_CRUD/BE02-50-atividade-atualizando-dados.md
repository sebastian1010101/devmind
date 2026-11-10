# BE02-50 — Atividade: Atualizando Dados

## Objetivo

Praticar `update`, `updateMany` e `upsert` numa camada de service — incluindo a diferença entre PATCH e PUT e operações atômicas.

## Services de atualização

```ts
// PATCH — atualização parcial
export async function atualizarUsuario(id: number, dados: Partial<Usuario>) {
  const usuario = await prisma.usuario.findUnique({ where: { id } });
  if (!usuario) throw new AppError("Usuário não encontrado", 404);

  return prisma.usuario.update({
    where: { id },
    data: dados,               // só o que veio no body
    select: { id: true, nome: true, email: true, atualizadoEm: true },
  });
}
```

```ts
// rota
router.patch("/usuarios/:id", async (req, res) => {
  const usuario = await atualizarUsuario(Number(req.params.id), req.body);
  return res.json(usuario);
});
```

## Operações atômicas — estoque

```ts
export async function venderProduto(produtoId: number, quantidade: number) {
  return prisma.$transaction(async (tx) => {
    const produto = await tx.produto.findUnique({ where: { id: produtoId } });

    if (!produto) throw new AppError("Produto não encontrado", 404);
    if (produto.estoque < quantidade) {
      throw new AppError("Estoque insuficiente", 422);
    }

    return tx.produto.update({
      where: { id: produtoId },
      data: { estoque: { decrement: quantidade } },
    });
  });
}
```

`decrement` dentro de transação = leitura + escrita atômicas — sem race condition.

## updateMany — ações em massa

```ts
// desativar usuários inativos há 1 ano
export async function arquivarInativos() {
  const limite = new Date();
  limite.setFullYear(limite.getFullYear() - 1);

  return prisma.usuario.updateMany({
    where: { ultimoAcesso: { lt: limite }, ativo: true },
    data: { ativo: false },
  });
  // { count: N } → log/retorno do total afetado
}
```

## upsert — perfil do usuário

```ts
export async function salvarPerfil(usuarioId: number, bio: string) {
  return prisma.perfil.upsert({
    where: { usuarioId },              // @unique → acha se existir
    create: { usuarioId, bio },
    update: { bio },
  });
}
```

## Validações a testar

```ts
// 404 — id inexistente
await atualizarUsuario(999, { nome: "X" });   // deve lançar AppError 404

// PATCH parcial não apaga outros campos
await atualizarUsuario(1, { telefone: "11-9999" });
// email, nome preservados

// decrement não vai negativo
await venderProduto(7, 100);   // estoque 5 → AppError 422
```

## Critérios de conclusão

1. PATCH parcial preserva campos não enviados
1. `decrement` atômico com checagem de estoque na transação
1. `updateMany` retornando `count` para log
1. `upsert` cobrindo create-e-update na mesma rota
1. 404 semântico em lugar de P2025 cru

## Resumo

- `Partial<T>` + `update` = PATCH idiomático
- Operações atômicas (`decrement`) em transação eliminam race conditions
- `updateMany` para ações em massa — retorna só contagem
- `upsert` simplifica "cria ou atualiza" por campo único
