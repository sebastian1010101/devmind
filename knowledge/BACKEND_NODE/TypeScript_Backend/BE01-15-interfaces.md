# BE01-15 — Interfaces

## O que é

Um **contrato** que define a forma de um objeto:

```typescript
interface Usuario {
  id: number;
  nome: string;
  email: string;
  ativo?: boolean;          // opcional
}

const u: Usuario = {
  id: 1,
  nome: "Ana",
  email: "ana@email.com",
};
```

Campos extras ou faltantes são erro em tempo de compilação.

## Interface em parâmetros e retornos

```typescript
function criarUsuario(dados: Omit<Usuario, "id">): Usuario {
  return { id: gerarId(), ...dados };
}

// Contrato de função
interface Repositorio<T> {
  buscar(id: number): T | undefined;
  salvar(item: T): T;
}
```

## extends — herança de interface

```typescript
interface Base {
  id: number;
  criadoEm: Date;
}

interface Usuario extends Base {
  nome: string;
  email: string;
}
// Usuario tem: id, criadoEm, nome, email
```

## Interface vs Type — a diferença prática

```typescript
interface Usuario { nome: string }
type Usuario = { nome: string }
```

| Interface | Type |
| --- | --- |
| Só descreve objetos | Qualquer tipo (unions, tuplas, primitivos) |
| `extends` para herdar | `&` para combinar |
| **Declaration merging** — declarações repetidas somam | Repetir dá erro |
| Pode ser implementada por classes | Não |

Convenção comum: `interface` para modelos de dados, `type` para unions e composições.

## Readonly e index signatures

```typescript
interface Config {
  readonly versao: string;   // não pode ser alterada depois
}

interface Dicionario {
  [chave: string]: number;   // qualquer chave string → number
}
```

## Interfaces no backend

```typescript
// Entidade (o que mora no "banco")
interface Livro {
  id: number;
  titulo: string;
  autor: string;
}

// DTO — o que a request traz (sem id, o servidor gera)
interface CriarLivroDTO {
  titulo: string;
  autor: string;
}

// Resposta formatada
interface LivroResponse {
  id: number;
  descricao: string;
}
```

Separar entidade / DTO / response evita vazar campos internos (ex.: senha) na API.

## Resumo

- Interface = contrato de forma — obrigatórios, opcionais (`?`), readonly
- `extends` compõe; `implements` liga a classe (BE01-25)
- Interface vs type: interface para modelos, type para unions/composições
- Separe entidade, DTO e response — controle o que entra e sai
