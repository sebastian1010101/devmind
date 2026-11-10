# FE05-46 — Interfaces

## O que é uma interface

Contrato que define a **forma de um objeto** — quais propriedades, de que tipo, quais são opcionais.

```typescript
interface Usuario {
  id: number;
  nome: string;
  email: string;
  admin?: boolean;    // opcional
  readonly cpf: string; // não pode mudar depois
}

function saudar(u: Usuario): string {
  return `Olá, ${u.nome}`;
}
```

## Estendendo — herança de interface

```typescript
interface Pessoa {
  nome: string;
  idade: number;
}

interface Aluno extends Pessoa {
  matricula: string;
  curso: string;
}

// Aluno tem: nome, idade, matricula, curso
```

## Múltipla herança

```typescript
interface Timestamps {
  criadoEm: Date;
  atualizadoEm: Date;
}

interface Permissoes {
  admin: boolean;
  mod: boolean;
}

interface Usuario extends Pessoa, Timestamps, Permissoes {
  email: string;
}
```

## Declaration merging — interface aberta

```typescript
interface Janela {
  titulo: string;
}

interface Janela {
  aberta: boolean; // MERGE — as duas se somam
}

// Janela tem: titulo + aberta
```

Útil para estender tipos de bibliotecas (ex: `Window`, `Request`).

## Implementando em classes

```typescript
interface Autenticavel {
  login(email: string, senha: string): Promise<boolean>;
  logout(): void;
}

class UsuarioService implements Autenticavel {
  async login(email: string, senha: string) {
    return true;
  }
  logout() {}
}
```

## Interface vs Type — a diferença real

```typescript
// Interface — pode ser estendida, merged, implementada
interface Usuario { nome: string; }
interface Usuario { idade: number; } // merge ok
interface Admin extends Usuario {}    // extends ok

// Type — mais flexível, mas não faz merge
type Usuario = { nome: string; };
type Usuario = { idade: number; }; // ❌ erro — duplicado
type Admin = Usuario & { perm: boolean }; // intersection
```

| | Interface | Type |
| --- | --- | --- |
| Objetos | ✅ | ✅ |
| Extensão | `extends` | `&` |
| Merge | ✅ | ❌ |
| Union/Primitivos | ❌ | ✅ |
| Classes (`implements`) | ✅ | ⚠️ |

## Index signatures — campos dinâmicos

```typescript
interface Estoque {
  [produto: string]: number; // qualquer chave string → number
}

const est: Estoque = {
  "mouse": 10,
  "teclado": 5
};
```

## Call signatures — interface de função

```typescript
interface Operacao {
  (a: number, b: number): number;
}

const soma: Operacao = (a, b) => a + b;
```

## Readonly e opcional juntos

```typescript
interface Config {
  readonly api: string;
  readonly versao: string;
  debug?: boolean;
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `interface` para union | Union é `type` — interface é objeto |
| Merge acidental | Nomeie diferente ou use `type` |
| `implements` em type complexo | Interface é mais clara pra classes |
| Index signature genérica demais | `Record<K, V>` mais específico |

## Resumo

- Interface define contrato de objeto — propriedades, tipos, opcionais
- `extends` herda; múltiplas interfaces acumulam
- Declaration merging soma declarações do mesmo nome
- `implements` em classes; index signature para campos dinâmicos
