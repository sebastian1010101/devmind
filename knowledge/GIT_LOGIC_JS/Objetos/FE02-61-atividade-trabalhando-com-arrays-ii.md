# FE02-61 — Atividade: Trabalhando com Arrays II

## Objetivo da Atividade

Aprofundar a manipulação de matrizes bidimensionais e arrays aninhados, realizando extrações de dados e somatórios de linhas e colunas.

---

## Enunciado do Desafio

Dado o mapa de notas de uma escola representado como uma matriz onde cada linha representa um aluno e cada coluna representa uma matéria (Português, Matemática e História):

```javascript
const boletimClasse = [
  ["Lucas", [8.0, 9.0, 7.5]],
  ["Beatriz", [10.0, 9.5, 9.0]],
  ["Mateus", [6.5, 7.0, 8.0]]
];
```

Construa um programa que:
1. Imprima o nome de cada aluno e a sua nota específica em Matemática (segunda matéria, índice 1).
2. Crie uma função `calcularMediaAluno(notas)` que receba o array de notas do aluno e retorne sua média aritmética.
3. Imprima o boletim final completo com a média individual de cada aluno da turma.

---

## Solução de Referência

```javascript
const boletimClasse = [
  ["Lucas", [8.0, 9.0, 7.5]],
  ["Beatriz", [10.0, 9.5, 9.0]],
  ["Mateus", [6.5, 7.0, 8.0]]
];

function calcularMediaAluno(notas) {
  let soma = 0;
  for (const nota of notas) {
    soma += nota;
  }
  return Number((soma / notas.length).toFixed(2));
}

console.log("=== NOTAS DE MATEMÁTICA (COLUNA ÍNDICE 1) ===");
for (let i = 0; i < boletimClasse.length; i++) {
  const nomeAluno = boletimClasse[i][0];
  const notaMatematica = boletimClasse[i][1][1];
  console.log(`${nomeAluno}: ${notaMatematica}`);
}

console.log("\n=== BOLETIM COMPLETO COM MÉDIAS ===");
for (let i = 0; i < boletimClasse.length; i++) {
  const nome = boletimClasse[i][0];
  const notas = boletimClasse[i][1];
  const mediaFinal = calcularMediaAluno(notas);
  const statusAprovacao = mediaFinal >= 7.0 ? "Aprovado" : "Recuperação";

  console.log(`${nome.padEnd(10)} | Média: ${mediaFinal.toFixed(2)} | Situação: ${statusAprovacao}`);
}
```
