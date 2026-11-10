# BE01-22 — Classes: Herança

## O que é

Uma classe **filha** (subclasse) herda atributos e métodos da **pai** (superclasse) com `extends`:

```typescript
class Animal {
  constructor(public nome: string) {}

  emitirSom(): string {
    return "...";
  }
}

class Cachorro extends Animal {
  emitirSom(): string {
    return "Au au!";
  }
}

const rex = new Cachorro("Rex");
rex.nome;        // "Rex" — herdado
rex.emitirSom(); // "Au au!" — sobrescrito
```

## `super` — chamando a classe pai

Obrigatório no construtor da filha **antes** de usar `this`:

```typescript
class ContaBancaria {
  constructor(
    public titular: string,
    protected saldo: number
  ) {}
}

class ContaCorrente extends ContaBancaria {
  constructor(titular: string, saldo: number, private limite: number) {
    super(titular, saldo);        // inicializa a parte pai
    this.limite = limite;         // depois, a parte filha
  }
}
```

`super.metodo()` também chama a versão pai de dentro da sobrescrita:

```typescript
class ContaPoupanca extends ContaBancaria {
  extrato(): string {
    return `${super.constructor.name} — saldo: ${this.saldo}`;
  }
}
```

## Sobrescrita (override)

A filha redefine um método da pai:

```typescript
class Notificacao {
  enviar(msg: string): string {
    return `Enviando: ${msg}`;
  }
}

class NotificacaoEmail extends Notificacao {
  override enviar(msg: string): string {   // 'override' documenta a intenção
    return `📧 Email: ${msg}`;
  }
}
```

`override` (opcional mas recomendado) faz o TS reclamar se você sobrescrever algo que não existe na pai.

## protected — visível na hierarquia

```typescript
class Conta {
  protected saldo = 0;   // filhas veem; fora da classe, não
}

class ContaCorrente extends Conta {
  aplicarTaxa() {
    this.saldo -= 10;    // ✅ filha acessa
  }
}
```

| Modificador | Na classe | Nas filhas | Fora |
| --- | --- | --- | --- |
| `public` | ✅ | ✅ | ✅ |
| `protected` | ✅ | ✅ | ❌ |
| `private` | ✅ | ❌ | ❌ |

## Herança no backend

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 400
  ) {
    super(message);
  }
}

class NotFoundError extends AppError {
  constructor(recurso: string) {
    super(`${recurso} não encontrado`, 404);
  }
}

throw new NotFoundError("Usuário");
```

Erros customizados são o uso clássico — `AppError` carrega `statusCode`, filhas especializam.

## Composição vs herança

```typescript
// Herança — "é um"
class ContaCorrente extends ContaBancaria {}

// Composição — "tem um" — frequentemente melhor
class Pedido {
  constructor(private pagamento: ProcessadorPagamento) {}
}
```

Regra: herança para hierarquias reais e rasas; composição para montar comportamentos.

## Resumo

- `extends` herda; `super()` inicializa o pai antes do `this`
- `override` documenta sobrescritas e pega typos
- `protected` = visível na hierarquia, invisível fora
- `AppError extends Error` — o padrão de herança do backend
