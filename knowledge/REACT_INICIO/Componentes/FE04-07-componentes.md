# FE04-07 — Componentes

## O que é um componente

Componente é uma **função JavaScript que retorna JSX** — o bloco fundamental de construção de toda aplicação React. Cada componente encapsula um pedaço da interface: sua estrutura, seu estilo e sua lógica.

```jsx
function Botao() {
  return <button>Clique aqui</button>;
}
```

## A analogia dos blocos de montar

Uma interface React é uma árvore de componentes aninhados — cada um com uma responsabilidade:

```text
App
├── Header
│   ├── Logo
│   ├── Nav
│   │   ├── NavItem (×3)
│   └── BotaoTema
├── Main
│   ├── ListaProdutos
│   │   ├── CardProduto (×N)
│   │   └── Paginacao
│   └── Sidebar
└── Footer
```

Cada caixa é um componente — isolado, testável, reutilizável.

## Anatomia de um componente

```jsx
// 1. Nome em PascalCase (obrigatório — distingue de tags HTML)
// 2. Recebe props (objeto) como parâmetro
// 3. Retorna JSX
function Saudacao(props) {
  return <h1>Olá, {props.nome}!</h1>;
}
```

## Componente vs elemento

Distinção que confunde quem começa:

- **Componente** — a função/classe: `function Botao() { ... }`
- **Elemento** — o que o componente retorna: `<button>...</button>`

```jsx
// 'Botao' é o componente
function Botao() {
  // <button> é o elemento JSX que ele retorna
  return <button>Clique</button>;
}

// <Botao /> é um "elemento de componente" — a invocação
<Botao />
```

## Usando componentes

Componentes se invocam como tags HTML, com letra maiúscula:

```jsx
function App() {
  return (
    <div>
      <Header />       {/* componente — PascalCase */}
      <Main />
      <Footer />
    </div>
  );
}
```

**Regra crítica**: letra maiúscula = componente; letra minúscula = tag HTML nativa.

```jsx
<Botao />   // React busca a função Botao
<button />  // React renderiza a tag HTML nativa
```

## Componente com lógica interna

Componentes podem ter variáveis, funções e lógica antes do `return`:

```jsx
function Contador() {
  // Lógica JavaScript normal
  const agora = new Date();
  const hora = agora.getHours();
  const saudacao = hora < 12 ? "Bom dia" : hora < 18 ? "Boa tarde" : "Boa noite";

  function handleClick() {
    console.log("Clicou!");
  }

  return (
    <div>
      <h1>{saudacao}</h1>
      <button onClick={handleClick}>Clique</button>
    </div>
  );
}
```

## Composição — componentes dentro de componentes

O padrão fundamental do React é **composição** — componentes pequenos formando componentes maiores:

```jsx
function Logo() {
  return <img src="/logo.png" alt="Logo" />;
}

function Nav() {
  return (
    <nav>
      <a href="/">Home</a>
      <a href="/sobre">Sobre</a>
    </nav>
  );
}

function Header() {
  return (
    <header>
      <Logo />
      <Nav />
    </header>
  );
}
```

## Componentes de função vs classe

React tem duas formas de declarar componentes:

```jsx
// ✅ Função — o padrão moderno, use sempre
function Botao() {
  return <button>Clique</button>;
}

// ❌ Classe — legado, raramente usado hoje
class Botao extends React.Component {
  render() {
    return <button>Clique</button>;
  }
}
```

Componentes de classe existem em código legado e ainda funcionam — mas todo código novo usa funções. Os hooks (`useState`, `useEffect`) só funcionam em componentes de função.

## Um arquivo por componente

A convenção padrão é um componente por arquivo, nomeado igual à função:

```text
src/
├── App.jsx            ← componente raiz
├── components/
│   ├── Header.jsx     ← exporta function Header
│   ├── Nav.jsx        ← exporta function Nav
│   ├── Button.jsx     ← exporta function Button
│   └── Card.jsx       ← exporta function Card
```

## Regras dos componentes

- **PascalCase** — `MeuComponente`, nunca `meuComponente`
- **Retorna JSX** — ou `null` para não renderizar nada
- **Puro** — a mesma entrada (props) deve gerar a mesma saída (JSX)
- **Um trabalho** — se um componente faz muita coisa, divida

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| `function botao()` minúsculo | React trata como tag HTML — não renderiza o componente |
| Esquecer o `return` | Componente retorna `undefined` — nada na tela |
| Chamar `Botao()` em vez de `<Botao />` | Funciona, mas React perde rastreio e otimizações |
| Lógica dentro do JSX em `{}` | Statements (`if`, `for`) não cabem em `{}` — use expressões |
