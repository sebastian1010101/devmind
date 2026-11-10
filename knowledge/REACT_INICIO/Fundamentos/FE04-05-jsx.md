# FE04-05 — JSX

## O que é JSX

**JSX** (JavaScript XML) é a sintaxe que permite escrever markup dentro de JavaScript — a forma declarativa de descrever a UI em React. Parece HTML, mas é JavaScript: cada tag JSX é compilada em uma chamada `React.createElement()`.

```jsx
const elemento = <h1>Olá, React!</h1>;

// O que o JSX vira "por baixo dos panos":
const elemento = React.createElement("h1", null, "Olá, React!");
```

## JSX não é HTML — as diferenças

### class → className

`class` é palavra reservada do JavaScript (de classes) — no JSX, usa `className`:

```jsx
// ❌ Erro — 'class' é reservado
<div class="container">

// ✅ Correto
<div className="container">
```

### for → htmlFor

```jsx
// ❌ 'for' é reservado (loops)
<label for="nome">

// ✅
<label htmlFor="nome">
```

### Atributos em camelCase

```jsx
// HTML          →  JSX
onclick            onClick
onchange           onChange
tabindex           tabIndex
readonly           readOnly
maxlength          maxLength
```

### Estilo inline é objeto

```jsx
// ❌ String, como no HTML
<div style="color: red; font-size: 16px">

// ✅ Objeto JS com camelCase
<div style={{ color: "red", fontSize: "16px" }}>
```

As chaves duplas `{{}}`: a externa marca "expressão JavaScript", a interna é o objeto literal.

## Expressões JavaScript com {}

Tudo entre chaves `{}` é avaliado como JavaScript:

```jsx
const nome = "Ana";
const idade = 28;

<h1>Olá, {nome}!</h1>                    // variável
<p>Ano que vem: {idade + 1}</p>          // expressão
<p>{formatarNome(nome)}</p>              // chamada de função
<p>{idade >= 18 ? "Adulto" : "Menor"}</p> // ternário
<img src={imagemUrl} />                  // atributo dinâmico
```

### O que pode ir dentro de {}

```jsx
{variavel}                               // ✅ valor
{2 + 2}                                  // ✅ expressão
{condicao && <p>Sim</p>}                 // ✅ JSX como expressão
{lista.map(i => <li>{i}</li>)}           // ✅ expressão de array
{funcao()}                               // ✅ chamada

{let x = 5}                              // ❌ declaração — não é expressão
{if (x) {}}                              // ❌ if não é expressão
{for (...)}                              // ❌ for não é expressão
```

Regra: dentro de `{}` só cabem **expressões** (coisas que produzem um valor). Statements (`if`, `for`, `let`) precisam ficar fora ou ser convertidos em ternários/`&&`/`.map()`.

## Um único elemento raiz

Componentes devem retornar **um** elemento raiz (ou Fragment):

```jsx
// ❌ Erro — dois elementos soltos
return (
  <h1>Título</h1>
  <p>Texto</p>
)

// ✅ Um elemento pai
return (
  <div>
    <h1>Título</h1>
    <p>Texto</p>
  </div>
)

// ✅ Fragment — sem criar div extra no DOM
return (
  <>
    <h1>Título</h1>
    <p>Texto</p>
  </>
)
```

## Self-closing tags

Tags sem filhos precisam fechar com `/>`:

```jsx
// ✅ Correto
<img src="foto.jpg" />
<input type="text" />
<br />
<Componente />

// ❌ Inválido em JSX
<img src="foto.jpg">
<input type="text">
```

## Comentários

```jsx
return (
  <div>
    {/* Comentário em JSX é um comentário JS dentro de {} */}
    <p>Conteúdo</p>
  </div>
)
```

## Renderizando tipos diferentes

```jsx
return (
  <div>
    {"string renderiza"}            {/* texto */}
    {42}                            {/* número */}
    {true}                          {/* nada aparece */}
    {null}                          {/* nada aparece */}
    {undefined}                     {/* nada aparece */}
    {[1, 2, 3]}                     {/* renderiza "123" — concatena */}
    {{ nome: "Ana" }}               {/* ERRO — objetos não renderizam */}
  </div>
)
```

`true`, `false`, `null` e `undefined` são ignorados — é o que permite `condicao && <Elemento />` funcionar.

## Atributos dinâmicos

```jsx
const imagem = {
  src: "foto.jpg",
  alt: "Foto do produto",
  largura: 200
};

// ✅ Espalha atributos
<img src={imagem.src} alt={imagem.alt} width={imagem.largura} />

// ✅ Spread de props
<img {...imagem} />
```

## JSX dentro de variáveis e funções

JSX é uma expressão — pode ser guardada, retornada, passada:

```jsx
const cabecalho = <h1>Bem-vindo</h1>;

function renderRodape() {
  return <footer>© 2024</footer>;
}

const lista = [
  <li key="1">Item 1</li>,
  <li key="2">Item 2</li>
];
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `class=` | `className=` |
| `for=` | `htmlFor=` |
| Dois elementos raiz | Envolva em `<div>` ou `<>` |
| `<img>` sem fechar | `<img />` — self-closing obrigatório |
| `if` dentro de `{}` | Use ternário `? :` ou `&&` |
| `onclick` minúsculo | `onClick` — camelCase |
| `style="..."` string | `style={{...}}` objeto |
| `{objeto}` direto | Objetos não renderizam — use `{objeto.nome}` |

## Resumo

JSX é a "cola" entre JavaScript e markup — expressões entre `{}`, camelCase em atributos, um elemento raiz, self-closing tags. É a sintaxe que torna a UI declarativa e o componente React legível como uma árvore de elementos.
