# FE02-50 — Tarefa 1

## Objetivo da Tarefa

Avaliar a compreensão de manipulação de listas, busca de elementos por critérios de texto e formatação de saídas estruturadas.

---

## Enunciado do Desafio

Construa uma função chamada `pesquisarLivrosPorAutor(catalogo, autorDesejado)` que:

1. Recebe uma lista de títulos de livros e o nome do autor que o usuário deseja buscar.
2. Cada item do catálogo é uma string no formato: `"Título do Livro - Nome do Autor"`.
3. A função deve percorrer o catálogo e retornar um novo array contendo apenas os títulos dos livros correspondentes ao autor informado.
4. Caso nenhum livro seja encontrado, retorne uma mensagem informando que não há registros correspondentes.

---

## Solução de Referência

```javascript
// Catálogo de teste:
const acervoBiblioteca = [
  "O Senhor dos Anéis - J.R.R. Tolkien",
  "O Hobbit - J.R.R. Tolkien",
  "Harry Potter e a Pedra Filosofal - J.K. Rowling",
  "1984 - George Orwell",
  "A Revolução dos Bichos - George Orwell",
  "Silmarillion - J.R.R. Tolkien"
];

function pesquisarLivrosPorAutor(catalogo, autorDesejado) {
  const livrosEncontrados = [];
  const autorBusca = autorDesejado.trim().toLowerCase();

  for (const item of catalogo) {
    // Divide a string no traço separador
    const partes = item.split(" - ");
    const titulo = partes[0].trim();
    const autor = partes[1].trim();

    if (autor.toLowerCase() === autorBusca) {
      livrosEncontrados.push(titulo);
    }
  }

  if (livrosEncontrados.length === 0) {
    return `Nenhum livro encontrado para o autor: "${autorDesejado}".`;
  }

  return livrosEncontrados;
}

// Testes:
console.log("Livros de George Orwell:", pesquisarLivrosPorAutor(acervoBiblioteca, "George Orwell"));
// ["1984", "A Revolução dos Bichos"]

console.log("Livros de Machado de Assis:", pesquisarLivrosPorAutor(acervoBiblioteca, "Machado de Assis"));
// "Nenhum livro encontrado para o autor: 'Machado de Assis'."
```
