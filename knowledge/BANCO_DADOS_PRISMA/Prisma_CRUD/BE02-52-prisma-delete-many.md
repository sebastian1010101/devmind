# BE02-52 — Prisma: Delete Many

## O básico

```ts
const resultado = await prisma.log.deleteMany({
  where: { criadoEm: { lt: dataLimite } },
});
// → { count: 480 } — quantos foram removidos
```

`DELETE FROM ... WHERE` — remove todos que casam; retorna a contagem.

## vs delete

| `delete` | `deleteMany` |
| --- | --- |
| `where` único, um registro | `where` aberto, N registros |
| Retorna o objeto | Retorna `{ count }` |
| P2025 se não existir | `{ count: 0 }` — sem erro |

## Sem where — a tabela inteira

```ts
await prisma.sessao.deleteMany({});
// ou simplesmente
await prisma.sessao.deleteMany();
```

É o `DELETE sem WHERE` — equivale a `TRUNCATE` na prática (menos o reset de sequence). Intencional só em cleanup/seed/testes.

## Com filtros de relação

```ts
// remover itens de pedidos cancelados
await prisma.itemPedido.deleteMany({
  where: { pedido: { status: "cancelado" } },
});

// usuários que nunca fizeram pedido
await prisma.usuario.deleteMany({
  where: { pedidos: { none: {} } },
});
```

## Em cascata manual — junção explícita

```ts
// remover estudante + suas matrículas
await prisma.$transaction([
  prisma.matricula.deleteMany({ where: { estudanteId: id } }),
  prisma.estudante.delete({ where: { id } }),
]);
```

Quando não há `onDelete: Cascade`, o `deleteMany` dos filhos vem antes na transação.

## Limpeza programada — jobs

```ts
// típico em cron/rotina de manutenção
export async function limparSessoesExpiradas() {
  const { count } = await prisma.sessao.deleteMany({
    where: { expiraEm: { lt: new Date() } },
  });
  console.log(`${count} sessões expiradas removidas`);
}
```

## Performance

- `deleteMany` gera **um** DELETE — muito mais rápido que deletar em loop
- Em tabelas gigantes considere lotes: filtre por faixa de data/id e repita
- `TRUNCATE` real (incluindo reset de sequence) só via `$executeRaw`:

```ts
await prisma.$executeRaw`TRUNCATE TABLE logs RESTART IDENTITY`;
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Esperar `P2025` quando nada casa | `deleteMany` retorna `{ count: 0 }` — sem erro |
| Filhos bloqueando | FKs sem cascade impedem — delete filhos antes |
| Sequence não reseta | `deleteMany` não reinicia SERIAL — `TRUNCATE ... RESTART IDENTITY` |
| Deletar sem where por acidente | Confirme o filtro — `deleteMany()` vazio limpa a tabela |

## Resumo

- `deleteMany({ where })` = `DELETE ... WHERE` — retorna `{ count }`
- Sem `where` limpa a tabela — mas não reseta sequences
- Combine em transação com `delete` do pai quando não há cascade
- Para `TRUNCATE` de verdade: `$executeRaw`
