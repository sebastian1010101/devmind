# FE03-47 — Arrow Function

## A Sintaxe de Seta (`=>`)

As **Arrow Functions** são uma das marcas visuais mais reconhecíveis do JavaScript moderno. Elas fornecem uma sintaxe muito mais limpa para escrever funções, especialmente quando utilizadas como funções anônimas de callback.

---

## Variações de Sintaxe

### 1. Sintaxe Completa com Bloco `{}`
Quando a função possui múltiplas linhas e exige a palavra-chave `return`:

```javascript
const calcularMedia = (nota1, nota2) => {
  const soma = nota1 + nota2;
  return soma / 2;
};
```

### 2. Retorno Implícito de Uma Linha (Implicit Return)
Quando a função executa apenas uma única instrução, **as chaves `{}` e o `return` podem ser omitidos**:

```javascript
// Retorna automaticamente o resultado de (a * b):
const multiplicar = (a, b) => a * b;

console.log(multiplicar(6, 7)); // 42
```

### 3. Parâmetro Único sem Parênteses
Se houver exatamente um único parâmetro, os parênteses `()` tornam-se opcionais:

```javascript
const calcularDobro = n => n * 2;
```

### 4. Retornando Objetos Literais de Forma Implícita
Para retornar um objeto literal com retorno implícito, envolva o objeto entre parênteses `({})` para evitar que o JS confunda as chaves do objeto com o corpo de um bloco de função:

```javascript
const criarUsuario = (nome, email) => ({ nome, email, ativo: true });

console.log(criarUsuario("Sebastián", "seba@dev.com"));
```

---

## A Diferença Crítica do `this` Léxico

Arrow Functions **NÃO possuem seu próprio contexto de `this`**. Elas capturam o `this` do escopo envolvente onde foram definidas (*escopo léxico*):

- **Perfeito para:** callbacks internas, métodos de array (`.map()`, `.filter()`), temporizadores (`setTimeout`) e ouvintes onde você deseja manter o `this` da classe ou função pai.
- **Inadequado para:** métodos de objetos literais tradicionais onde o `this` deveria apontar para o próprio objeto, ou funções construtoras com `new`.
