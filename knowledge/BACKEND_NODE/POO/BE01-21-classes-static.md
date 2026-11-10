# BE01-21 — Classes: Static

## O que é

Membro que pertence à **classe**, não às instâncias — existe uma vez só, compartilhado:

```typescript
class Matematica {
  static PI = 3.14159;

  static dobro(n: number): number {
    return n * 2;
  }
}

// Sem new — chama direto na classe
Matematica.PI;         // 3.14159
Matematica.dobro(5);   // 10
```

## Static vs instância

```typescript
class Contador {
  static total = 0;        // um só, da classe
  valor = 0;               // um por instância

  incrementar() {
    this.valor++;
    Contador.total++;      // acessa static pelo nome da classe
  }
}

const a = new Contador();
const b = new Contador();
a.incrementar();
b.incrementar();
b.incrementar();

a.valor;          // 1
b.valor;          // 2
Contador.total;   // 3 — soma de todas as instâncias
```

`this.valor` = da instância. `Contador.total` = da classe.

## Usos comuns

### Contador de instâncias

```typescript
class Usuario {
  static totalCriados = 0;

  constructor(public nome: string) {
    Usuario.totalCriados++;
  }
}
```

### Factory methods

```typescript
class Usuario {
  private constructor(
    public nome: string,
    public role: string
  ) {}

  static criarAdmin(nome: string) {
    return new Usuario(nome, "ADMIN");
  }

  static criarComum(nome: string) {
    return new Usuario(nome, "USER");
  }
}

const admin = Usuario.criarAdmin("Ana"); // construtor privado força o factory
```

### Utilitários sem estado

```typescript
class Validador {
  static emailValido(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}

Validador.emailValido("a@b.com"); // true
```

## No backend — onde aparece

```typescript
// Constantes de configuração
class AppConfig {
  static readonly PORT = 3000;
  static readonly PREFIX = "/api";
}

// Registry de erros
class AppError extends Error {
  static naoEncontrado(recurso: string) {
    return new AppError(`${recurso} não encontrado`, 404);
  }
}
```

## Limitações

- `static` não acessa `this` de instância — não existe instância no contexto
- Estado estático compartilhado é global disfarçado — cuidado com efeitos colaterais
- Em testes, estado static persiste entre testes — reset manual necessário

## Resumo

- `static` = da classe, não da instância — chama sem `new`
- Usos: contadores, factories, utilitários, constantes
- `Classe.membro` para acessar; `this` não vê statics
- Cuidado: static compartilhado é estado global
