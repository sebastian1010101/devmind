# BE01-19 — Classes: Construtor

## O que é

O método especial que roda **automaticamente no `new`** — inicializa a instância:

```typescript
class Usuario {
  nome: string;
  email: string;

  constructor(nome: string, email: string) {
    this.nome = nome;
    this.email = email;
  }
}

const ana = new Usuario("Ana", "ana@email.com"); // pronto numa linha
```

Sem construtor, cada atributo era setado separadamente depois do `new` — verboso e permite objeto "pela metade".

## Shorthand do TS — parâmetros com modificadores

```typescript
// Forma longa
class Usuario {
  nome: string;
  email: string;
  constructor(nome: string, email: string) {
    this.nome = nome;
    this.email = email;
  }
}

// Shorthand — o modificador já declara E atribui
class Usuario {
  constructor(
    public nome: string,
    public email: string,
    private senha: string
  ) {}
}
```

`public`, `private`, `protected`, `readonly` no parâmetro = cria o atributo automaticamente.

## Validação no construtor

O construtor é o lugar de garantir que o objeto **nasce válido**:

```typescript
class Produto {
  constructor(
    public nome: string,
    public preco: number
  ) {
    if (!nome.trim()) throw new Error("Nome obrigatório");
    if (preco <= 0) throw new Error("Preço deve ser positivo");
  }
}

new Produto("", -10); // ❌ lança erro — objeto inválido nunca existe
```

## Valores padrão e opcionais

```typescript
class Tarefa {
  constructor(
    public titulo: string,
    public concluida: boolean = false,   // padrão
    public criadoEm: Date = new Date()
  ) {}
}

new Tarefa("Estudar");                    // usa os defaults
new Tarefa("Estudar", true);              // sobrescreve
```

## readonly — atributo imutável

```typescript
class Pedido {
  constructor(
    public readonly id: number,  // ninguém muda depois do construtor
    public total: number
  ) {}
}

const p = new Pedido(1, 99.9);
p.id = 2; // ❌ erro de compilação
```

## Sobrecarga — não existe em TS

Diferente de Java/C#, TS não tem múltiplos construtores. Alternativas:

```typescript
// Parâmetros opcionais
constructor(nome: string, email?: string) {}

// Ou factory estática
class Usuario {
  static criarComEmail(email: string) {
    return new Usuario("sem-nome", email);
  }
}
```

## Resumo

- `constructor` roda no `new` — inicializa e valida
- `public/private/readonly` no parâmetro = atributo automático
- Valide no construtor — objeto inválido nem nasce
- Sem sobrecarga: use defaults, opcionais ou factory estática
