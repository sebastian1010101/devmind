# FE04-09 — Atividade: Meus Primeiros Componentes

## Objetivo

Criar os primeiros componentes React — quebrando uma página em blocos reutilizáveis e praticando exportação/importação.

## Estrutura do exercício

```text
src/
├── App.jsx
├── main.jsx
└── components/
    ├── Header.jsx
    ├── Nav.jsx
    ├── Card.jsx
    └── Footer.jsx
```

## Passo 1 — Componente Nav

```jsx
// src/components/Nav.jsx
function Nav() {
  return (
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/sobre">Sobre</a></li>
        <li><a href="/contato">Contato</a></li>
      </ul>
    </nav>
  );
}

export default Nav;
```

## Passo 2 — Componente Header (compõe Nav)

```jsx
// src/components/Header.jsx
import Nav from "./Nav";

function Header() {
  return (
    <header>
      <h1>Meu Site</h1>
      <Nav />
    </header>
  );
}

export default Header;
```

## Passo 3 — Componente Card

```jsx
// src/components/Card.jsx
function Card() {
  return (
    <article className="card">
      <h2>Título do Card</h2>
      <p>Descrição do conteúdo do card aqui.</p>
      <button>Saiba mais</button>
    </article>
  );
}

export default Card;
```

## Passo 4 — Componente Footer

```jsx
// src/components/Footer.jsx
function Footer() {
  const ano = new Date().getFullYear();

  return (
    <footer>
      <p>© {ano} — Todos os direitos reservados</p>
    </footer>
  );
}

export default Footer;
```

## Passo 5 — App orquestra tudo

```jsx
// src/App.jsx
import Header from "./components/Header";
import Card from "./components/Card";
import Footer from "./components/Footer";

function App() {
  return (
    <div>
      <Header />

      <main>
        <Card />
        <Card />
        <Card />
      </main>

      <Footer />
    </div>
  );
}

export default App;
```

## Desafios extras

### Desafio A — Card com dados diferentes

Transforme `Card` em componente reutilizável com props:

```jsx
function Card({ titulo, descricao }) {
  return (
    <article className="card">
      <h2>{titulo}</h2>
      <p>{descricao}</p>
      <button>Saiba mais</button>
    </article>
  );
}

// No App:
<Card titulo="React" descricao="Biblioteca para UIs" />
<Card titulo="CSS" descricao="Estilização" />
<Card titulo="JS" descricao="Lógica" />
```

### Desafio B — Nav com dados dinâmicos

```jsx
function Nav() {
  const links = [
    { texto: "Home", href: "/" },
    { texto: "Sobre", href: "/sobre" },
    { texto: "Contato", href: "/contato" }
  ];

  return (
    <nav>
      <ul>
        {links.map(link => (
          <li key={link.href}>
            <a href={link.href}>{link.texto}</a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

### Desafio C — estilização básica

```jsx
// src/App.css
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.card button {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}
```

## Critérios de verificação

- Um componente por arquivo, em `src/components/`
- `export default` em cada componente
- Nomes em PascalCase (`Header`, `Nav`, `Card`)
- `App` importa e compõe os componentes
- `key` presente no `.map()` de listas
- Lógica JS fora do JSX (variáveis antes do `return`)

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| `import { Header }` com `export default` | `undefined` — sem chaves para default |
| `function nav()` minúsculo | React trata como tag HTML |
| `Card()` em vez de `<Card />` | Funciona, mas perde benefícios do React |
| `new Date()` dentro do JSX | Funciona, mas lógica fica suja — extraia antes |
