# BE01-24 — Classes: Níveis de Acesso

## Os modificadores

```typescript
class Conta {
  public titular: string;      // qualquer lugar acessa (é o default)
  protected saldo: number;     // classe + subclasses
  private senha: string;       // só dentro desta classe
  readonly criadoEm: Date;     // só leitura após inicialização
}
```

| Modificador | Classe | Subclasse | Fora |
| --- | --- | --- | --- |
| `public` (default) | ✅ | ✅ | ✅ |
| `protected` | ✅ | ✅ | ❌ |
| `private` | ✅ | ❌ | ❌ |
| `readonly` | leitura em todos os lugares onde visível | | |

## private — encapsulamento real

```typescript
class ContaBancaria {
  private saldo = 0;

  depositar(valor: number): void {
    if (valor <= 0) throw new Error("Valor inválido");
    this.saldo += valor;
  }

  obterSaldo(): number {
    return this.saldo;
  }
}

const conta = new ContaBancaria();
conta.saldo = 1000000;  // ❌ não compila — private
conta.depositar(100);   // ✅ caminho correto
```

Ninguém burla a regra de negócio — o saldo só muda pelos métodos.

## Getters e setters — acesso controlado

```typescript
class Usuario {
  private _email: string;

  get email(): string {
    return this._email;
  }

  set email(valor: string) {
    if (!valor.includes("@")) throw new Error("Email inválido");
    this._email = valor;
  }
}

const u = new Usuario();
u.email = "ana@email.com";   // usa o set — valida
u.email = "invalido";        // 💥 erro
console.log(u.email);        // usa o get
```

Parece propriedade, executa como método — validação sem mudar a sintaxe de acesso.

## private (TS) vs `#` (JS nativo)

```typescript
class Segredo {
  private tsPrivado = "a";   // privado só em compile-time
  #jsPrivado = "b";          // privado de verdade — runtime também
}
```

`#campo` é o privado do JavaScript moderno — `private` do TS não impede acesso em runtime via `(obj as any).campo`.

## readonly — imutabilidade

```typescript
class Pedido {
  readonly id: number;
  readonly itens: Item[];

  constructor(id: number, itens: Item[]) {
    this.id = id;
    this.itens = itens;
  }
}

pedido.id = 2;        // ❌ readonly
pedido.itens.push(x); // ⚠️ compila! readonly protege a REFERÊNCIA, não o conteúdo
```

Para conteúdo também imutável: `private itens` + getter retornando cópia.

## Diretriz prática

```text
Tudo private por padrão → exponha o mínimo via métodos públicos
```

API pequena = menos pontos de acoplamento = manutenção fácil.

## Resumo

- `public`/`protected`/`private` controlam visibilidade; `readonly` trava reatribuição
- Getters/setters validam sem mudar a sintaxe de propriedade
- `private` é compile-time; `#` é privado de verdade em runtime
- Comece tudo privado — exponha só o necessário
