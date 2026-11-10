# FE02-52 — Introdução a Objetos

## O que é um Objeto em JavaScript?

Um **Objeto** é uma estrutura de dados fundamental utilizada para mapear entidades do mundo real em código. Enquanto arrays agrupam valores ordenados por índices numéricos (`0, 1, 2...`), objetos agrupam coleções não ordenadas de propriedades no formato de **chave e valor** (*key-value pairs*).

```javascript
// Criando um objeto com a sintaxe de literal de objeto {}:
const usuario = {
  nome: "Sebastián Gomez",
  idade: 26,
  cidade: "Curitiba",
  ativo: true
};
```

---

## Formas de Acessar Propriedades de um Objeto

Existem duas maneiras fundamentais de ler e modificar propriedades:

### 1. Notação de Ponto (Dot Notation) — Padrão e Mais Limpa

Utilizada quando você já sabe o nome exato da propriedade no momento da escrita do código:

```javascript
console.log(usuario.nome);   // "Sebastián Gomez"
console.log(usuario.cidade); // "Curitiba"

// Modificação e criação de nova propriedade:
usuario.idade = 27;
usuario.profissao = "Desenvolvedor Front-End";
```

### 2. Notação de Colchetes (Bracket Notation)

Obrigatória quando o nome da propriedade:
- É dinâmico e vem armazenado em uma variável.
- Contém caracteres especiais ou espaços.

```javascript
const campoDesejado = "cidade";

// Acessando dinamicamente através do valor da variável:
console.log(usuario[campoDesejado]); // "Curitiba"
```

---

## Adicionando e Removendo Propriedades

```javascript
const produto = {
  nome: "Mouse Gamer",
  preco: 180.00
};

// Adicionando nova propriedade:
produto.estoque = 30;

// Removendo propriedade com o operador delete:
delete produto.estoque;

console.log(produto); // { nome: "Mouse Gamer", preco: 180 }
```
