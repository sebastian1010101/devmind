# BE01-26 — `type` para Tipos Personalizados

## Criando aliases de tipo

```typescript
type ID = number;
type Email = string;
type Status = "PENDENTE" | "PAGO" | "CANCELADO";

type Usuario = {
  id: ID;
  email: Email;
  status: Status;
};
```

`type` nomeia qualquer tipo — dá semântica e reutilização.

## O que `type` faz que `interface` não faz

```typescript
// Union
type Resultado = Sucesso | Falha;

// Primitivo
type ID = string | number;

// Tupla
type Coordenada = [number, number];

// Função
type Handler = (req: Req, res: Res) => void;

// Literal
type MetodoHTTP = "GET" | "POST" | "PUT" | "DELETE";
```

Interface só descreve objetos — `type` cobre tudo.

## Interseção com `&`

```typescript
type Base = { id: number; criadoEm: Date };
type Auditavel = { atualizadoPor: string };

type Entidade = Base & Auditavel;
// { id, criadoEm, atualizadoPor }
```

Equivalente ao `extends` de interface, mas funciona com qualquer combinação.

## Tipos compostos

```typescript
// Union de objetos (discriminated)
type Forma =
  | { tipo: "circulo"; raio: number }
  | { tipo: "retangulo"; largura: number; altura: number };

function area(f: Forma): number {
  if (f.tipo === "circulo") return Math.PI * f.raio ** 2;
  return f.largura * f.altura; // TS já sabe que é retangulo
}
```

## type vs interface — a decisão

| Use `type` para | Use `interface` para |
| --- | --- |
| Unions (`A \| B`) | Modelos de dados |
| Interseções complexas | Contratos de classe (`implements`) |
| Tuplas, primitivos, funções | Hierarquias com `extends` |
| Mapeamentos (`Record`, mapped types) | Declaration merging |

Na prática, para objetos simples os dois funcionam igual — consistência do time importa mais.

## Tipos utilitários com `type`

```typescript
type ParcialUsuario = Partial<Usuario>;       // tudo opcional
type SemId = Omit<Usuario, "id">;             // menos o id
type SoContato = Pick<Usuario, "email">;      // só alguns campos
type UsuarioSomenteLeitura = Readonly<Usuario>;
```

## Resumo

- `type` nomeia qualquer tipo: objeto, union, tupla, função, literal
- `&` intersecta, `|` une — composição de tipos
- Interface para modelos/contratos; type para unions e composições
- Utilities (`Partial`, `Omit`, `Pick`) derivam tipos sem repetir
