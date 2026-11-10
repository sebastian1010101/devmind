# BE01-23 — Classes: Polimorfismo

## O que é

**"Muitas formas"** — objetos de classes diferentes respondem ao mesmo método, cada um do seu jeito:

```typescript
class Pagamento {
  processar(valor: number): string {
    return `Processando R$${valor}`;
  }
}

class PagamentoPix extends Pagamento {
  override processar(valor: number): string {
    return `Pix instantâneo de R$${valor}`;
  }
}

class PagamentoCartao extends Pagamento {
  override processar(valor: number): string {
    return `Cartão em 12x de R$${valor / 12}`;
  }
}
```

## O poder: tratar pelo tipo pai

```typescript
function finalizarCompra(pagamento: Pagamento, valor: number) {
  console.log(pagamento.processar(valor)); // qual funciona? o da subclasse real
}

finalizarCompra(new PagamentoPix(), 100);    // "Pix instantâneo de R$100"
finalizarCompra(new PagamentoCartao(), 100); // "Cartão em 12x..."
```

A função conhece só a **abstração** (`Pagamento`) — em runtime, o método correto de cada subclasse roda.

## Polimorfismo em coleções

```typescript
const metodos: Pagamento[] = [
  new PagamentoPix(),
  new PagamentoCartao(),
];

metodos.forEach((m) => console.log(m.processar(50)));
// Cada um processa do seu jeito — mesma interface, comportamentos diferentes
```

## Classe abstrata — molde incompleto

```typescript
abstract class Pagamento {
  // Método abstrato: a filha É OBRIGADA a implementar
  abstract processar(valor: number): string;

  // Método concreto: herdado como está
  log(valor: number) {
    console.log(`[${new Date().toISOString()}] ${this.processar(valor)}`);
  }
}

class PagamentoPix extends Pagamento {
  processar(valor: number) { return `Pix de R$${valor}`; }
}

// new Pagamento(); // ❌ classe abstrata não instancia
```

## Polimorfismo no backend

```typescript
abstract class Repositorio<T> {
  abstract buscar(id: number): T | undefined;
  abstract salvar(item: T): T;
}

class RepositorioMemoria<T extends { id: number }> extends Repositorio<T> {
  private dados: T[] = [];

  buscar(id: number) {
    return this.dados.find((d) => d.id === id);
  }

  salvar(item: T) {
    this.dados.push(item);
    return item;
  }
}

// Depois: class RepositorioPrisma<T> extends Repositorio<T> — troca a implementação
// sem mudar quem usa
```

Service depende da abstração `Repositorio<T>` — troca memória por Prisma sem reescrever nada.

## Polimorfismo vs `if/switch`

```typescript
// Sem polimorfismo — if cresce a cada tipo novo
function processar(tipo: string, valor: number) {
  if (tipo === "pix") return `Pix...`;
  if (tipo === "cartao") return `Cartão...`;
}

// Com polimorfismo — novo tipo = nova classe, zero edição no código existente
```

Open/Closed: aberto para extensão (novas subclasses), fechado para modificação.

## Resumo

- Mesmo método, comportamento por classe — chamador usa só o tipo pai
- `abstract` = contrato obrigatório para as filhas + código compartilhado
- No backend: repositórios, erros, handlers — troca implementação sem reescrever
- Elimina cadeias de `if` por tipo — extensão por novas classes
