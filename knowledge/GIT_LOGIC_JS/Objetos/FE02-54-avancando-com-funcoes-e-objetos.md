# FE02-54 — Avançando com Funções e Objetos

## Passando Objetos como Argumentos de Funções

Funções em JavaScript podem receber objetos inteiros como parâmetros. Isso evita a necessidade de criar funções com dezenas de argumentos soltos e difíceis de memorizar a ordem.

```javascript
// Ruim: função com muitos parâmetros soltos (fácil errar a ordem)
function criarUsuario(nome, idade, email, cidade, uf, cep, ativo) { ... }

// Excelente: função recebendo um único objeto de configuração
function exibirFichaCadastral(cliente) {
  console.log(`Cliente: ${cliente.nome} | E-mail: ${cliente.email} | Cidade: ${cliente.cidade}`);
}

const novoCliente = {
  nome: "Lucas Pereira",
  email: "lucas@exemplo.com",
  cidade: "São Paulo"
};

exibirFichaCadastral(novoCliente);
```

---

## Desestruturação de Objetos (Destructuring Assignment — ES6)

A desestruturação permite extrair propriedades específicas de um objeto e atribuí-las diretamente a variáveis individuais de forma concisa:

```javascript
const configuracao = {
  tema: "escuro",
  notificacoes: true,
  linguagem: "pt-BR"
};

// Sintaxe de desestruturação:
const { tema, linguagem } = configuracao;

console.log(tema);      // "escuro"
console.log(linguagem); // "pt-BR"
```

### Desestruturação Direta nos Parâmetros de Funções

É uma das práticas mais comuns e elegantes do JavaScript moderno:

```javascript
function calcularPrecoComFrete({ preco, frete, desconto = 0 }) {
  return (preco - desconto) + frete;
}

const itemPedido = {
  titulo: "Livro de JavaScript",
  preco: 80.00,
  frete: 15.00,
  desconto: 10.00
};

console.log("Total a pagar: R$", calcularPrecoComFrete(itemPedido)); // 85
```
