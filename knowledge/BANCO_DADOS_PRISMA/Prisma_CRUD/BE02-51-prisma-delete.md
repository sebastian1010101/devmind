# BE02-51 — Prisma: Delete

## O básico

```ts
const deletado = await prisma.usuario.delete({
  where: { id: 1 },
});
// retorna o objeto que foi removido
```

`where` por campo único — como `update`, o delete é direcionado a um registro identificado.

## Fluxo seguro — 404 primeiro

```ts
export async function deletarUsuario(id: number) {
  const usuario = await prisma.usuario.findUnique({ where: { id } });
  if (!usuario) throw new AppError("Usuário não encontrado", 404);

  await prisma.usuario.delete({ where: { id } });
  // ou confie no P2025:
}
```

```ts
// alternativa: deixar o Prisma lançar
try {
  await prisma.usuario.delete({ where: { id: 999 } });
} catch (e) {
  // P2025: Record to delete does not exist → 404
}
```

## Na rota — status code

```ts
router.delete("/usuarios/:id", async (req, res) => {
  await deletarUsuario(Number(req.params.id));
  return res.status(204).send();    // No Content — sem body
});
```

`204` é o padrão para DELETE bem-sucedido — a rota não retorna JSON.

## Deletando com relações

```sql
-- o banco barra se houver filhos:
DELETE FROM usuarios WHERE id = 1;
-- violates foreign key constraint (P2003/P2014 no Prisma)
```

```ts
// delete falha: usuário tem pedidos
await prisma.usuario.delete({ where: { id: 1 } });
// P2014/P2003 — a menos que onDelete: Cascade na FK
```

Opções:

1. **Cascade no schema** — `onDelete: Cascade` na relação
1. **Deletar filhos antes** — na transação:

```ts
await prisma.$transaction([
  prisma.pedido.deleteMany({ where: { usuarioId: id } }),
  prisma.usuario.delete({ where: { id } }),
]);
```

## Soft delete — quando o dado não pode sumir

```prisma
model Usuario {
  // ...
  deletadoEm DateTime? @map("deletado_em")
}
```

```ts
// "deletar" = marcar
await prisma.usuario.update({
  where: { id },
  data: { deletadoEm: new Date() },
});

// listar = filtrar os vivos
await prisma.usuario.findMany({
  where: { deletadoEm: null },
});
```

Soft delete protege histórico e referências — auditoria, "lixeira", recuperação.

## Erros comuns

| Erro | Correção |
| --- | --- |
| P2025/P2014 em produção | Mapear para 404/409 no middleware de erro |
| FK bloqueando o delete | `onDelete: Cascade` ou delete filhos primeiro |
| Retornar 200 com objeto deletado | `204 No Content` é o padrão REST |
| Hard delete quando precisa de histórico | Soft delete com `deletadoEm` |

## Resumo

- `delete({ where: único })` remove e retorna o objeto
- Id inexistente → P2025 → 404
- FK bloqueia delete de pai — cascade no schema ou filhos primeiro
- `204` na rota; soft delete quando o dado precisa sobreviver
