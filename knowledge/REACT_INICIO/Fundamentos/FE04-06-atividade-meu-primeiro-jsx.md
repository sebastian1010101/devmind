# FE04-06 — Atividade: Meu Primeiro JSX

## Objetivo

Criar o primeiro componente React com JSX — aplicando expressões dinâmicas, atributos, className e renderização condicional básica.

## Setup

```bash
npm create vite@latest meu-primeiro-jsx -- --template react
cd meu-primeiro-jsx
npm install
npm run dev
```

## Desafio 1 — Cartão de perfil

Em `src/App.jsx`, monte um cartão de perfil usando variáveis JavaScript:

```jsx
function App() {
  const usuario = {
    nome: "Ana Silva",
    profissao: "Desenvolvedora Front-End",
    cidade: "Curitiba",
    idade: 28
  };

  return (
    <div className="perfil">
      <h1>{usuario.nome}</h1>
      <p>{usuario.profissao}</p>
      <p>{usuario.cidade} — {usuario.idade} anos</p>
    </div>
  );
}

export default App;
```

## Desafio 2 — Expressões calculadas

Adicione cálculos diretamente no JSX:

```jsx
function App() {
  const preco = 299.90;
  const quantidade = 3;
  const desconto = 0.15;

  const subtotal = preco * quantidade;
  const total = subtotal * (1 - desconto);

  return (
    <div className="carrinho">
      <p>Preço unitário: R$ {preco.toFixed(2)}</p>
      <p>Quantidade: {quantidade}</p>
      <p>Subtotal: R$ {subtotal.toFixed(2)}</p>
      <p>Desconto: {desconto * 100}%</p>
      <p>Total: R$ {total.toFixed(2)}</p>
    </div>
  );
}
```

## Desafio 3 — Lista dinâmica

Renderize uma lista de interesses com `.map()`:

```jsx
function App() {
  const interesses = ["React", "CSS", "JavaScript", "TypeScript"];

  return (
    <div className="interesses">
      <h2>Meus interesses</h2>
      <ul>
        {interesses.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Desafio 4 — Condicional com ternário

Mostre um status diferente conforme o estado:

```jsx
function App() {
  const logado = true;

  return (
    <div>
      <h1>{logado ? "Bem-vindo de volta!" : "Faça login"}</h1>
      <button>{logado ? "Sair" : "Entrar"}</button>
    </div>
  );
}
```

## Desafio 5 — Atributos dinâmicos

Imagem com src, alt e largura vindos de um objeto:

```jsx
function App() {
  const imagem = {
    src: "https://via.placeholder.com/300x200",
    alt: "Foto do produto",
    titulo: "Foto de perfil"
  };

  return (
    <div>
      <img
        src={imagem.src}
        alt={imagem.alt}
        title={imagem.titulo}
      />
    </div>
  );
}
```

## Desafio 6 — O componente completo

Junte tudo num cartão de perfil completo:

```jsx
function App() {
  const usuario = {
    nome: "Ana Silva",
    profissao: "Front-End Developer",
    cidade: "Curitiba",
    foto: "https://via.placeholder.com/150",
    online: true,
    interesses: ["React", "CSS", "JS"]
  };

  return (
    <div className="perfil">
      <img src={usuario.foto} alt={usuario.nome} />

      <h1>{usuario.nome}</h1>
      <span>{usuario.online ? "🟢 Online" : "⚫ Offline"}</span>

      <p>{usuario.profissao} — {usuario.cidade}</p>

      <ul>
        {usuario.interesses.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

## Critérios de verificação

- `{expressão}` para variáveis, cálculos e condicionais
- `className` em vez de `class`
- `key` presente em itens de lista (mesmo que por enquanto seja o índice)
- Um único elemento raiz no `return`
- Self-closing tags (`<img />`)
- O componente é uma função que retorna JSX

## Erros comuns a evitar

| Erro | Sintoma |
| --- | --- |
| `<img>` sem fechar | JSX exige self-closing |
| `class` em vez de `className` | Warning no console |
| Lista sem `key` | Warning: "Each child should have a unique key" |
| `{if(...)}` dentro do JSX | `if` não é expressão — use ternário ou `&&` |
| Objeto renderizado direto | `{usuario}` quebra — use `{usuario.nome}` |
| Múltiplos elementos soltos | Envolva em `<div>` ou `<>` |
