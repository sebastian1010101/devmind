# BE01-28 — Extends

## `extends` em interfaces

A interface filha **acrescenta** à pai:

```typescript
interface Entidade {
  id: number;
  criadoEm: Date;
}

interface Usuario extends Entidade {
  nome: string;
  email: string;
}
// Usuario: { id, criadoEm, nome, email }
```

## Múltipla herança de interfaces

```typescript
interface Timestamp {
  criadoEm: Date;
  atualizadoEm: Date;
}

interface SoftDelete {
  deletadoEm: Date | null;
}

interface Produto extends Timestamp, SoftDelete {
  id: number;
  nome: string;
  preco: number;
}
```

Interface herda de **várias** — composição de contratos.

## `extends` em classes (revisão)

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 400
  ) {
    super(message);
    this.name = "AppError";
  }
}
```

Classe herda de **uma** só — mas pode `implements` várias interfaces.

## `extends` em generics — restrição

Aqui `extends` significa **"deve satisfazer"**, não "herda de":

```typescript
// T pode ser qualquer coisa QUE TENHA id: number
function buscarPorId<T extends { id: number }>(lista: T[], id: number): T | undefined {
  return lista.find((item) => item.id === id);
}

buscarPorId(usuarios, 1);   // ✅ Usuario tem id
buscarPorId(["a", "b"], 1); // ❌ string não tem id
```

```typescript
// Repositório genérico — T deve ser uma entidade com id
class Repositorio<T extends { id: number }> {
  private dados: T[] = [];

  salvar(item: T): T {
    this.dados.push(item);
    return item;
  }

  buscar(id: number): T | undefined {
    return this.dados.find((d) => d.id === id);
  }
}
```

## extends em tipos condicionais

```typescript
// T estende U? Então X, senão Y
type EhString<T> = T extends string ? true : false;

type A = EhString<string>;  // true
type B = EhString<number>;  // false
```

A base de `infer` e dos utilitários avançados do TS.

## Resumo dos três usos de `extends`

| Contexto | Significado |
| --- | --- |
| `interface A extends B` | A inclui os membros de B |
| `class A extends B` | A herda implementação de B |
| `T extends U` em generic | T deve ser compatível com U |
| `T extends U ? X : Y` | condicional de tipo |

## Resumo

- Interfaces: herança múltipla de contratos com `extends`
- Classes: herança única de implementação + `super()`
- Generics: `T extends { id: number }` restringe o parâmetro
- Condicionais: a base dos tipos avançados do TS
