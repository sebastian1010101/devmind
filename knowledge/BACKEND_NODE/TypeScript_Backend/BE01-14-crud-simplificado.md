# BE01-14 — CRUD Simplificado

## O que é CRUD

As 4 operações básicas sobre dados:

| Operação | Significado | HTTP (prévia) |
| --- | --- | --- |
| **C**reate | criar registro | POST |
| **R**ead | ler/listar | GET |
| **U**pdate | atualizar | PUT/PATCH |
| **D**elete | remover | DELETE |

Aqui implementado **em memória** — array simples, sem banco ainda (vem no módulo 07).

## Modelo

```typescript
interface Produto {
  id: number;
  nome: string;
  preco: number;
}

const produtos: Produto[] = [];
let proximoId = 1;
```

## Create

```typescript
function criar(nome: string, preco: number): Produto {
  const produto: Produto = { id: proximoId++, nome, preco };
  produtos.push(produto);
  return produto;
}
```

## Read

```typescript
// Listar todos
function listar(): Produto[] {
  return produtos;
}

// Buscar por id — retorna Produto ou undefined
function buscar(id: number): Produto | undefined {
  return produtos.find((p) => p.id === id);
}
```

## Update

```typescript
function atualizar(
  id: number,
  dados: Partial<Omit<Produto, "id">>
): Produto | undefined {
  const produto = buscar(id);
  if (!produto) return undefined;

  Object.assign(produto, dados);
  return produto;
}
```

`Partial` = todos os campos opcionais; `Omit<Produto, "id">` = nunca muda o id.

## Delete

```typescript
function deletar(id: number): boolean {
  const indice = produtos.findIndex((p) => p.id === id);
  if (indice === -1) return false;

  produtos.splice(indice, 1);
  return true;
}
```

Retornar `boolean` deixa claro se o registro existia — alternativa: lançar erro (visto em BE01-49).

## Por que isso é "simplificado"

| Em memória | Com banco |
| --- | --- |
| Array local | Tabela PostgreSQL |
| Some ao reiniciar | Persistente |
| `find`/`splice` | `SELECT`/`DELETE` |
| Síncrono | Async (`await`) |

A **estrutura** é a mesma — funções de CRUD que serão trocadas por queries depois. Tipar bem agora facilita a migração.

## Resumo

- CRUD = Create/Read/Update/Delete — o vocabulário de todo backend
- Em memória: array + `find`/`findIndex`/`splice`
- `Partial<Omit<T, "id">>` — atualização parcial protegendo o id
- A mesma estrutura migra pra SQL/Prisma depois
