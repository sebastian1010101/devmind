# BE01-20 — Atividade: Criando uma Classe de Student

Exercício: modelar um estudante com atributos, construtor e métodos.

## Requisitos

- Nome, idade, curso
- Lista de notas
- Método para adicionar nota, calcular média e verificar aprovação

## Implementação

```typescript
class Student {
  private notas: number[] = [];

  constructor(
    public nome: string,
    public idade: number,
    public curso: string
  ) {
    if (idade < 0) throw new Error("Idade inválida");
  }

  adicionarNota(nota: number): void {
    if (nota < 0 || nota > 10) {
      throw new Error("Nota deve ser entre 0 e 10");
    }
    this.notas.push(nota);
  }

  calcularMedia(): number {
    if (this.notas.length === 0) return 0;
    const soma = this.notas.reduce((t, n) => t + n, 0);
    return soma / this.notas.length;
  }

  estaAprovado(): boolean {
    return this.calcularMedia() >= 7;
  }

  resumo(): string {
    return `${this.nome} (${this.curso}) — Média: ${this.calcularMedia().toFixed(1)}`;
  }
}
```

## Uso

```typescript
const ana = new Student("Ana", 20, "Full Stack");

ana.adicionarNota(8);
ana.adicionarNota(9.5);
ana.adicionarNota(7);

console.log(ana.resumo());        // "Ana (Full Stack) — Média: 8.2"
console.log(ana.estaAprovado());  // true

ana.notas.push(0);   // ❌ não compila — notas é private
ana.adicionarNota(15); // 💥 lança erro — nota inválida
```

## Desafios

1. `maiorNota(): number` e `menorNota(): number`
2. `static` contador de estudantes criados (prévia de BE01-21)
3. Getter `get quantidadeNotas()` — quantas notas lançadas
4. `removerNota(indice: number)` — remove se o índice existir

## Checklist

- [ ] `notas` privada — acesso só via método
- [ ] Construtor valida idade
- [ ] Método valida faixa da nota
- [ ] Média com `reduce`, divisão protegida contra array vazio
- [ ] Instâncias independentes — notas de Ana não vazam pra Bia

## Resumo

- Estado privado + métodos públicos = encapsulamento na prática
- Validações no construtor e nos métodos mantêm o objeto sempre válido
