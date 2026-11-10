# FE02-57 — Atividade: Trabalhando com Objetos II

## Objetivo da Atividade

Praticar o uso de objetos complexos com arrays internos, manipulação de métodos de cálculo acumulativo e iteração sobre propriedades usando laços.

---

## Enunciado do Desafio

Crie um objeto chamado `turma` que gerencie o desempenho acadêmico de um grupo de estudantes:

1. Propriedades:
   - `nomeCurso`: `"Desenvolvimento Web Full Stack"`
   - `alunos`: lista com pelo menos três nomes de alunos (`["Beatriz", "Carlos", "Mateus"]`).
   - `notas`: lista com as notas correspondentes de cada aluno (`[9.0, 7.5, 8.5]`).
2. Métodos:
   - `adicionarAluno(nome, nota)`: insere o novo aluno e sua respectiva nota nos arrays correspondentes.
   - `calcularMediaGeral()`: calcula e retorna a média aritmética de todas as notas da turma.
   - `exibirRelatorio()`: imprime uma tabela ou lista associando o nome de cada aluno à sua nota e exibe a média consolidada no final.

---

## Solução de Referência

```javascript
const turma = {
  nomeCurso: "Desenvolvimento Web Full Stack",
  alunos: ["Beatriz", "Carlos", "Mateus"],
  notas: [9.0, 7.5, 8.5],

  adicionarAluno(nome, nota) {
    this.alunos.push(nome);
    this.notas.push(nota);
    console.log(`Aluno ${nome} registrado com nota ${nota}.`);
  },

  calcularMediaGeral() {
    if (this.notas.length === 0) return 0;

    let soma = 0;
    for (const nota of this.notas) {
      soma += nota;
    }
    return Number((soma / this.notas.length).toFixed(2));
  },

  exibirRelatorio() {
    console.log(`=== BOLETIM GERAL: ${this.nomeCurso} ===`);
    for (let i = 0; i < this.alunos.length; i++) {
      console.log(`${i + 1}. ${this.alunos[i]} — Nota: ${this.notas[i]}`);
    }
    console.log("----------------------------------------");
    console.log(`Média Geral da Turma: ${this.calcularMediaGeral()}`);
    console.log("========================================\n");
  }
};

// Testes:
turma.exibirRelatorio();
turma.adicionarAluno("Mariana", 10.0);
turma.exibirRelatorio();
```
