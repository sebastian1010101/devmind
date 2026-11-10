# BE01-18 — Classes: Introdução

## Anatomia de uma classe

```typescript
class Usuario {
  // Atributos (propriedades)
  nome: string;
  email: string;

  // Método (comportamento)
  saudar(): string {
    return `Olá, ${this.nome}`;
  }
}
```

- `class` — o molde
- `new` — cria uma **instância** (objeto) a partir do molde
- `this` — referência à instância atual

## Instanciando

```typescript
const ana = new Usuario();
ana.nome = "Ana";
ana.email = "ana@email.com";

const bia = new Usuario();
bia.nome = "Bia";

ana.saudar(); // "Olá, Ana"
bia.saudar(); // "Olá, Bia" — cada instância tem seus dados
```

## Classe vs objeto literal

```typescript
// Objeto literal — um objeto solto, sem molde
const usuario = { nome: "Ana" };

// Classe — molde reutilizável com comportamentos
class Usuario {
  nome: string;
  saudar() { return `Olá, ${this.nome}`; }
}
```

Objeto literal = dados soltos. Classe = fábrica de objetos com métodos.

## `this` — a referência interna

```typescript
class Contador {
  valor: number = 0;

  incrementar() {
    this.valor++;        // this = esta instância
  }

  obter(): number {
    return this.valor;
  }
}

const c1 = new Contador();
const c2 = new Contador();
c1.incrementar();
c1.valor; // 1
c2.valor; // 0 — instâncias independentes
```

## Classe como tipo

A própria classe vira um tipo:

```typescript
function registrar(usuario: Usuario) { /* ... */ }

const lista: Usuario[] = [new Usuario(), new Usuario()];
```

## Métodos com parâmetros e retorno

```typescript
class Calculadora {
  somar(a: number, b: number): number {
    return a + b;
  }

  dividir(a: number, b: number): number {
    if (b === 0) throw new Error("Divisão por zero");
    return a / b;
  }
}
```

## Resumo

- `class` = molde; `new` = instância; `this` = a própria instância
- Atributos guardam estado, métodos definem comportamento
- A classe é também um tipo — use em parâmetros e arrays
- Próximo passo: `constructor` para inicializar na criação (BE01-19)
