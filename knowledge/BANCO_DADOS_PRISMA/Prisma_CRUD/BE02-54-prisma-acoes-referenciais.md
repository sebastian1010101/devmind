# BE02-54 — Prisma: Ações Referenciais

## O que são

O que acontece com os **filhos** quando o pai é deletado ou tem a PK alterada:

```prisma
model Livro {
  id      Int   @id @default(autoincrement())
  autor   Autor @relation(fields: [autorId], references: [id], onDelete: Cascade)
  autorId Int   @map("autor_id")
}
```

`onDelete`/`onUpdate` na `@relation` geram as cláusulas do SQL (`ON DELETE CASCADE` etc.).

## As opções

| Ação | Deletar o pai... | Atualizar a PK do pai... |
| --- | --- | --- |
| `Cascade` | Deleta os filhos junto | Propaga o novo valor |
| `Restrict` | **Bloqueia** se houver filhos | Bloqueia |
| `NoAction` | Idem (verificado no fim da transação) | Idem |
| `SetNull` | FK dos filhos vira `NULL` | FK vira `NULL` |
| `SetDefault` | FK assume o default | FK assume o default |

## Os três que importam na prática

### Cascade — "filhos morrem junto"

```prisma
autor Autor @relation(fields: [autorId], references: [id], onDelete: Cascade)
```

```ts
await prisma.autor.delete({ where: { id: 1 } });
// DELETE FROM livros WHERE autor_id = 1; DELETE FROM autores WHERE id = 1;
// uma chamada vira a limpeza completa — em transação implícita
```

Use quando o filho **não existe sem o pai**: itens de pedido, matrículas, tokens de sessão.

### Restrict — "protege o pai"

```prisma
autor Autor @relation(fields: [autorId], references: [id], onDelete: Restrict)
```

```ts
await prisma.autor.delete({ where: { id: 1 } });
// P2014: viola a FK — o banco recusa deixar livros órfãos
```

O padrão defensivo: força a aplicação a decidir conscientemente o destino dos filhos.

### SetNull — "órfãos permitidos"

```prisma
autor   Autor? @relation(fields: [autorId], references: [id], onDelete: SetNull)
autorId Int?   @map("autor_id")   // ← obrigatório ser nullable
```

```ts
await prisma.autor.delete({ where: { id: 1 } });
// livros ficam com autor_id = NULL — dados preservados, sem autor
```

A FK **precisa** ser `Int?` — `SetNull` em `Int` dá erro de schema.

## Escolhendo por domínio

```text
pedido → itens        → Cascade   (item sem pedido é lixo)
post   → comentários  → Cascade   (ou SetNull "comentário de usuário removido")
venda  → vendedor     → Restrict  (histórico fiscal não pode sumir)
tarefa → responsável  → SetNull   (tarefa continua sem dono)
```

## No migrate

Mudar `onDelete` gera migration — a FK é recriada:

```bash
npx prisma migrate dev --name cascade_livros
```

```sql
-- o SQL gerado:
ALTER TABLE livros DROP CONSTRAINT livros_autor_id_fkey;
ALTER TABLE livros ADD CONSTRAINT livros_autor_id_fkey
  FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE CASCADE;
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `SetNull` em FK `Int` | Precisa ser `Int?` — `SetNull` grava NULL |
| Delete de pai estourando P2014 | `Restrict`/`NoAction` ativos — escolha cascade ou delete filhos |
| Cascade em relação histórica | Vendas/pedidos raramente cascateiam — histórico importa |
| Assumir cascade sem conferir o schema | Leia a `@relation` — o comportamento está declarado nela |

## Resumo

- `onDelete`/`onUpdate` na `@relation` = ações referenciais do SQL
- `Cascade` deleta filhos; `Restrict`/`NoAction` bloqueiam; `SetNull` orfa; `SetDefault` reseta
- `SetNull` exige FK nullable (`Int?`)
- A escolha é de domínio: dados dependentes cascateiam, históricos restringem
