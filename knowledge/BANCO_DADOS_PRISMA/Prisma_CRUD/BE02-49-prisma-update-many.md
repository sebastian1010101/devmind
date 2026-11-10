# BE02-49 — Prisma: Update Many

## O básico

```ts
const resultado = await prisma.usuario.updateMany({
  where: { ativo: false, criadoEm: { lt: dataLimite } },
  data: { arquivado: true },
});
// → { count: 12 }
```

`UPDATE ... WHERE` — atualiza todos que casam; retorna só a **contagem**.

## vs update

| `update` | `updateMany` |
| --- | --- |
| `where` por campo único | `where` por qualquer critério |
| Um registro | N registros |
| Retorna o objeto | Retorna `{ count }` |
| `select`/`include` ok | Sem retorno dos dados |

## Mesmas operações de campo

```ts
await prisma.produto.updateMany({
  where: { categoria: "eletronicos" },
  data: { preco: { multiply: 1.10 } },    // reajuste de 10%
});

await prisma.carrinho.updateMany({
  where: { usuarioId: 7 },
  data: { abandonado: true },
});
```

## Sem where — a tabela toda

```ts
await prisma.config.updateMany({
  data: { versao: "2.0" },      // ⚠️ TODAS as linhas
});
```

Omitir `where` é legítimo quando intencional — mas é o `UPDATE` sem WHERE do SQL. Esteja certo.

## updateMany com filtro de relação

```ts
// arquivar livros de autores inativos
await prisma.livro.updateMany({
  where: { autor: { ativo: false } },
  data: { disponivel: false },
});
```

O `where` navega relações igual ao `findMany` (`some`/`every`/`none`/`is`).

## Quando precisa dos registros atualizados

`updateMany` não retorna os objetos. Opções:

```ts
// 1. updateMany + findMany
const ids = { in: [1, 2, 3] };
await prisma.usuario.updateMany({ where: { id: ids }, data: { ativo: true } });
const atualizados = await prisma.usuario.findMany({ where: { id: ids } });

// 2. ou update em loop/transação quando N é pequeno
await prisma.$transaction(
  ids.map(id => prisma.usuario.update({ where: { id }, data: { ativo: true } }))
);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Esperar os objetos de volta | `updateMany` retorna só `count` — faça `findMany` depois |
| `where` com campo não-único no `update` | O que precisa de filtro aberto é `updateMany` |
| Operação de campo dentro de updateMany não rola nested | `data` com `connect`/`create` não existe em many — use `update` por item |
| updateMany + include | Não existe — incluir é conceito de leitura |

## Resumo

- `updateMany({ where, data })` = `UPDATE ... WHERE` — retorna `{ count }`
- Aceita `increment`/`decrement`/filtros por relação — sem retorno dos objetos
- `where` omitido = atualiza a tabela inteira — confirme a intenção
- Precisou dos objetos? `findMany` com o mesmo `where` depois
