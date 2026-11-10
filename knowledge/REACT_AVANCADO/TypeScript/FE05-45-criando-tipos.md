# FE05-45 — Criando Tipos

## type — o alias de tipo

```typescript
type Usuario = {
  id: number;
  nome: string;
  email: string;
  admin?: boolean; // opcional
};

const ana: Usuario = {
  id: 1,
  nome: "Ana",
  email: "ana@email.com"
};
```

## Propriedades opcionais

```typescript
type Config = {
  tema: string;
  idioma: string;
  notificacoes?: boolean; // pode omitir
  apiUrl?: string;
};

const cfg: Config = { tema: "escuro", idioma: "pt" }; // ✅ sem notificacoes
```

## Union types — tipos compostos

```typescript
type Status = "pendente" | "aprovado" | "rejeitado";
type Id = string | number;
type Nullable<T> = T | null;
```

## Intersection types — juntando

```typescript
type Timestamps = {
  criadoEm: Date;
  atualizadoEm: Date;
};

type UsuarioCompleto = Usuario & Timestamps;
// tem: id, nome, email, admin?, criadoEm, atualizadoEm
```

## Tipos para funções

```typescript
type Operacao = (a: number, b: number) => number;

const somar: Operacao = (a, b) => a + b;
const subtrair: Operacao = (a, b) => a - b;

// callback
type Callback = (item: Produto) => void;
const executar = (itens: Produto[], cb: Callback) => itens.forEach(cb);
```

## Tipos utilitários — os helpers do TS

```typescript
// Partial — tudo opcional
type UsuarioEdicao = Partial<Usuario>;
// { id?, nome?, email?, admin? }

// Required — tudo obrigatório
type UsuarioCompleto = Required<Usuario>;

// Pick — seleciona campos
type UsuarioResumo = Pick<Usuario, "id" | "nome">;
// { id, nome }

// Omit — remove campos
type UsuarioSemSenha = Omit<Usuario, "senha">;

// Record — dicionário chave-valor
type Estoque = Record<string, number>;
// { "item1": 10, "item2": 5 }
```

## readonly — imutável

```typescript
type Config = {
  readonly versao: string;
  readonly api: string;
};

const cfg: Config = { versao: "1.0", api: "..." };
cfg.versao = "2.0"; // ❌ erro — readonly
```

## Type vs Interface — quando cada um

```typescript
// Interface — objetos, extensível
interface Animal {
  nome: string;
}
interface Cachorro extends Animal { // extends
  raca: string;
}

// Type — unions, primitivos, funções
type Status = "a" | "b";
type Coordenada = [number, number];
type Handler = (e: Event) => void;
```

| Use `interface` | Use `type` |
| --- | --- |
| Objetos/classes | Unions, primitivos |
| Pode precisar de `extends` | Intersections complexas |
| Pode precisar de declaration merging | Funções, tuplas |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `any` onde cabe `type` | Defina o tipo — mesmo que simples |
| Interface vs type confusos | Regra: objeto → interface; union/primitivo → type |
| `Partial` quando precisa de `Omit` | `Partial` deixa tudo opcional — cuidado |
| `readonly` esquecido | Útil para config e constantes |

## Resumo

- `type Nome = { ... }` cria um alias reutilizável
- `?` para opcionais; `|` union; `&` intersection
- `Partial`, `Pick`, `Omit`, `Record` — utilitários essenciais
- Interface para objetos extensíveis; type para unions e primitivos
