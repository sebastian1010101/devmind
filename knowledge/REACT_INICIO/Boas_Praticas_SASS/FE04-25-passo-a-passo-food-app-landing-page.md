# FE04-25 — Passo a Passo: Food App Landing Page

## O projeto

Landing page de um app de delivery — o exercício integra tudo do módulo até aqui: componentes, props, listas, CSS Modules e organização de arquitetura.

## Estrutura planejada

```text
Food App
├── Header       → logo + nav + botão de download
├── Hero         → título, subtítulo, CTA, imagem
├── Features     → 3-4 cards de diferenciais
├── Menu         → grid de pratos populares
├── Testimonials → depoimentos de clientes
└── Footer       → links, redes sociais, copyright
```

## Arquitetura de arquivos

```text
src/
├── components/
│   ├── Header/
│   │   ├── Header.jsx
│   │   └── Header.module.css
│   ├── Hero/
│   ├── FeatureCard/
│   ├── MenuSection/
│   ├── MenuItem/
│   ├── Testimonial/
│   └── Footer/
├── data/
│   └── menu.js          ← dados dos pratos
├── App.jsx
└── index.css            ← reset + variáveis
```

## Implementação

### Dados separados — `data/menu.js`

```javascript
export const pratos = [
  { id: 1, nome: "Burger Clássico", preco: 32, emoji: "🍔" },
  { id: 2, nome: "Pizza Margherita", preco: 45, emoji: "🍕" },
  { id: 3, nome: "Sushi Combo", preco: 58, emoji: "🍣" },
  { id: 4, nome: "Salada Caesar", preco: 28, emoji: "🥗" }
];
```

### Header com composição

```jsx
// components/Header/Header.jsx
import styles from "./Header.module.css";

function Header() {
  return (
    <header className={styles.header}>
      <span className={styles.logo}>🍔 FoodApp</span>
      <nav>
        <a href="#menu">Menu</a>
        <a href="#sobre">Sobre</a>
        <a href="#contato">Contato</a>
      </nav>
      <button className={styles.cta}>Baixar App</button>
    </header>
  );
}
```

### Hero — a dobra principal

```jsx
function Hero() {
  return (
    <section className={styles.hero}>
      <div>
        <h1>Comida boa, <br />entrega rápida</h1>
        <p>Seus restaurantes favoritos na palma da mão.</p>
        <button className={styles.cta}>Pedir agora</button>
      </div>
      <span className={styles.emoji}>🍔</span>
    </section>
  );
}
```

### Menu — lista de dados

```jsx
// components/MenuSection/MenuSection.jsx
import { pratos } from "../../data/menu";
import MenuItem from "../MenuItem/MenuItem";

function MenuSection() {
  return (
    <section id="menu">
      <h2>Mais pedidos</h2>
      <div className={styles.grid}>
        {pratos.map(p => <MenuItem key={p.id} {...p} />)}
      </div>
    </section>
  );
}
```

```jsx
// components/MenuItem/MenuItem.jsx
function MenuItem({ nome, preco, emoji }) {
  return (
    <article className={styles.item}>
      <span className={styles.emoji}>{emoji}</span>
      <h3>{nome}</h3>
      <p>R$ {preco.toFixed(2)}</p>
      <button>Pedir</button>
    </article>
  );
}
```

### App orquestrando

```jsx
import Header from "./components/Header/Header";
import Hero from "./components/Hero/Hero";
import MenuSection from "./components/MenuSection/MenuSection";
import Footer from "./components/Footer/Footer";

function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <MenuSection />
      </main>
      <Footer />
    </>
  );
}
```

## Lições de arquitetura

| Decisão | Por quê |
| --- | --- |
| Dados em `data/menu.js` | Separa conteúdo de apresentação |
| Uma pasta por componente | CSS Modules colado ao JSX |
| `App` só orquestra | Cada seção é autônoma |
| Props nomeadas | Contrato legível (`nome`, `preco`) |

## Extensões possíveis

- Seção de depoimentos com `Testimonial`
- Footer com links e ícones sociais
- Estado no menu (`useState` para carrinho) — vem nos próximos tópicos
- Deploy na Vercel como exercício final
