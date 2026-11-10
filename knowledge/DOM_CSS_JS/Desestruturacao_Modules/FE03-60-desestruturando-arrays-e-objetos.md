# FE03-60 — Desestruturando Arrays e Objetos

## O que é

**Destructuring** (desestruturação) é a sintaxe do ES6 que extrai valores de arrays e propriedades de objetos diretamente para variáveis — numa única linha, sem acessos repetidos por índice ou ponto.

```javascript
// ❌ Antes — acesso repetitivo
const nome = usuario.nome;
const idade = usuario.idade;

// ✅ Com desestruturação
const { nome, idade } = usuario;
```

## Desestruturação de objetos

A desestruturação de objetos usa **nomes de propriedades** — a ordem não importa:

```javascript
const pessoa = { nome: "Ana", idade: 28, cidade: "Curitiba" };

const { cidade, nome } = pessoa; // ordem irrelevante
console.log(nome);   // "Ana"
console.log(cidade); // "Curitiba"
```

### Renomeando variáveis

Quando o nome da propriedade conflita com uma variável existente, use `prop: novoNome`:

```javascript
const { nome: nomeCompleto } = pessoa;
console.log(nomeCompleto); // "Ana" — a propriedade 'nome' foi para 'nomeCompleto'
```

### Valores padrão

Se a propriedade não existir, defina um fallback com `=`:

```javascript
const { profissao = "não informada" } = pessoa;
// "não informada" — pessoa não tem 'profissao'
```

### Objetos aninhados

```javascript
const empresa = {
  nome: "Kenzie",
  endereco: { cidade: "Curitiba", estado: "PR" }
};

const { endereco: { cidade, estado } } = empresa;
// cidade = "Curitiba", estado = "PR"
// ⚠️ 'endereco' em si NÃO vira variável — só 'cidade' e 'estado'
```

### Em parâmetros de função

O uso mais poderoso — extrair só o necessário direto na assinatura:

```javascript
// ❌ Recebe o objeto inteiro, acessa dentro
function exibir(usuario) {
  console.log(`${usuario.nome}, ${usuario.idade} anos`);
}

// ✅ Extrai só o que usa — a assinatura documenta o contrato
function exibir({ nome, idade }) {
  console.log(`${nome}, ${idade} anos`);
}

exibir({ nome: "Ana", idade: 28, cargo: "dev" }); // cargo ignorado
```

## Desestruturação de arrays

Em arrays, a posição define a variável (diferente de objetos, onde é o nome):

```javascript
const cores = ["vermelho", "verde", "azul"];

const [primeira, segunda] = cores;
// primeira = "vermelho", segunda = "verde"
```

### Pulando posições

```javascript
const [, , terceira] = cores; // vírgulas vazias pulam posições
// terceira = "azul"
```

### Valores padrão em arrays

```javascript
const [a, b, c = "padrão"] = ["x", "y"];
// a = "x", b = "y", c = "padrão"
```

### O truque do swap

Trocar variáveis sem variável temporária:

```javascript
let x = 1, y = 2;
[x, y] = [y, x];
// x = 2, y = 1
```

## Rest operator na desestruturação

`...resto` captura tudo que não foi extraído:

```javascript
// Em arrays — captura os elementos restantes
const [head, ...tail] = [1, 2, 3, 4];
// head = 1, tail = [2, 3, 4]

// Em objetos — captura as propriedades restantes
const { nome, ...outros } = { nome: "Ana", idade: 28, cidade: "Curitiba" };
// nome = "Ana", outros = { idade: 28, cidade: "Curitiba" }
```

### Excluindo propriedades (padrão de API)

```javascript
const usuario = { id: 1, nome: "Ana", senha: "123", email: "a@a.com" };

// Remove 'senha' do objeto retornado
const { senha, ...dadosPublicos } = usuario;
// dadosPublicos = { id: 1, nome: "Ana", email: "a@a.com" }
```

## Casos de uso profissionais

### Retorno múltiplo de função

```javascript
function dividir(a, b) {
  return [Math.floor(a / b), a % b];
}

const [quociente, resto] = dividir(10, 3);
// quociente = 3, resto = 1
```

### useState do React

O padrão mais famoso de desestruturação de array:

```javascript
const [contador, setContador] = useState(0);
// useState retorna [valor, setter] — desestrutura na chamada
```

### Configurações com defaults

```javascript
function conectar({ host = "localhost", porta = 3000, ssl = false }) {
  // parâmetros nomeados — a ordem dos argumentos não importa
}

conectar({ porta: 8080 }); // host e ssl usam os padrões
```

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| `const { a } = null` | `TypeError` — proteja com `= {}` → `const { a } = obj \|\| {}` |
| Desestruturar sem declarar | `x, y = [1,2]` sem `let`/`const` precisa de `(...)` — `{a, b} = obj` precisa de parênteses |
| `const [a] = {b: 1}` | Desestruturação de array em objeto falha — tipos devem combinar |
| Renomear com `:` errado | `nome: novo` — o nome da **propriedade** vai à esquerda, a variável à direita |
