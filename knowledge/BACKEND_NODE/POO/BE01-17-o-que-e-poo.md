# BE01-17 — O que é POO

## Programação Orientada a Objetos

Um paradigma que organiza o código em **objetos** — entidades que juntam **dados** (atributos) e **comportamentos** (métodos):

```typescript
// Sem POO — dados e funções soltos
const nome = "Ana";
const saldo = 100;
function sacar(valor: number) { /* ... */ }

// Com POO — tudo junto num objeto
class ContaBancaria {
  nome: string;
  saldo: number;

  sacar(valor: number) {
    if (valor <= this.saldo) this.saldo -= valor;
  }
}
```

## Os 4 pilares

| Pilar | Ideia | Exemplo |
| --- | --- | --- |
| **Encapsulamento** | Dados protegidos, acesso controlado | `private saldo` + método `sacar()` |
| **Herança** | Classe filha reutiliza a pai | `ContaCorrente extends Conta` |
| **Polimorfismo** | Mesmo método, comportamentos diferentes | `calcularTaxa()` diferente por tipo de conta |
| **Abstração** | Esconde complexidade, expõe o essencial | `conta.sacar(50)` sem saber a lógica interna |

## POO no backend — onde aparece

```text
Classes      →  Services, Controllers, Models
Encapsulamento → dados do banco ficam privados na classe
Herança      →  BaseController, AppError extends Error
Interfaces   →  contratos entre camadas (repositório)
```

Frameworks como NestJS são **100% orientados a objetos** — classes, injeção de dependência, decorators.

## POO vs funcional

```typescript
// POO — estado dentro do objeto
class Carrinho {
  private itens: Item[] = [];
  adicionar(item: Item) { this.itens.push(item); }
  total() { return this.itens.reduce((t, i) => t + i.preco, 0); }
}

// Funcional — dados e funções separadas
const adicionar = (itens: Item[], item: Item): Item[] => [...itens, item];
const total = (itens: Item[]): number => itens.reduce((t, i) => t + i.preco, 0);
```

TS suporta os dois — o curso usa POO porque espelha frameworks enterprise e organiza bem camadas.

## Resumo

- POO = objetos com dados + comportamentos juntos
- 4 pilares: encapsulamento, herança, polimorfismo, abstração
- No backend: Services, Controllers, Errors customizados são classes
- TS permite POO e funcional — escolha por contexto
