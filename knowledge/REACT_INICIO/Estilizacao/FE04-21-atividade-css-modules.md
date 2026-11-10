# FE04-21 — Atividade: Estilizando com CSS Modules

## Objetivo

Estilizar um componente de produto usando CSS Modules — aplicando classes locais, composição e classes condicionais.

## Estrutura

```text
src/
├── components/
│   └── ProductCard/
│       ├── ProductCard.jsx
│       ├── ProductCard.module.css
│       └── index.js
├── App.jsx
└── index.css           ← variáveis globais
```

## Variáveis globais

```css
/* src/index.css */
:root {
  --cor-primaria: #3498db;
  --cor-texto: #222;
  --cor-borda: #e0e0e0;
  --raio: 8px;
}
```

## O componente

```jsx
// src/components/ProductCard/ProductCard.jsx
import styles from "./ProductCard.module.css";

function ProductCard({ nome, preco, foto, emPromocao }) {
  return (
    <article className={styles.card}>
      <img src={foto} alt={nome} className={styles.imagem} />

      <div className={styles.corpo}>
        <h3 className={styles.titulo}>{nome}</h3>

        <p className={styles.preco}>
          {emPromocao && <span className={styles.tagPromo}>Promoção</span>}
          R$ {preco.toFixed(2)}
        </p>

        <button
          className={`${styles.botao} ${emPromocao ? styles.botaoPromo : ""}`}
        >
          Comprar
        </button>
      </div>
    </article>
  );
}

export default ProductCard;
```

## O CSS Module

```css
/* src/components/ProductCard/ProductCard.module.css */
.card {
  border: 1px solid var(--cor-borda);
  border-radius: var(--raio);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.imagem {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.corpo {
  padding: 1rem;
}

.titulo {
  font-size: 1.1rem;
  color: var(--cor-texto);
  margin-bottom: 0.5rem;
}

.preco {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--cor-primaria);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tagPromo {
  background: #e74c3c;
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.botao {
  margin-top: 1rem;
  width: 100%;
  padding: 0.6rem;
  background: var(--cor-primaria);
  color: white;
  border-radius: 6px;
  transition: background 0.2s;
}

.botao:hover {
  background: #2980b9;
}

.botaoPromo {
  background: #e74c3c;
}

.botaoPromo:hover {
  background: #c0392b;
}
```

## Uso no App

```jsx
import ProductCard from "./components/ProductCard";

function App() {
  const produtos = [
    { id: 1, nome: "Teclado", preco: 150, foto: "...", emPromocao: true },
    { id: 2, nome: "Mouse", preco: 80, foto: "...", emPromocao: false }
  ];

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem" }}>
      {produtos.map(p => <ProductCard key={p.id} {...p} />)}
    </div>
  );
}
```

## index.js — re-export

```javascript
// src/components/ProductCard/index.js
export { default } from "./ProductCard";
```

## Desafios extras

### Desafio A — variante escura

```css
.cardEscuro {
  composes: card;
  background: #1a1a2e;
  color: white;
}
```

```jsx
<article className={escuro ? styles.cardEscuro : styles.card}>
```

### Desafio B — badge de estoque

```jsx
<span className={estoque === 0 ? styles.esgotado : styles.disponivel}>
  {estoque === 0 ? "Esgotado" : `${estoque} un.`}
</span>
```

## Critérios de verificação

- Arquivo `.module.css` ao lado do componente
- `import styles` — nunca `import "./X.module.css"` sem variável
- Classes camelCase no objeto `styles`
- Condicionais com template string — não `className` concatenado solto
- `composes` para estilos compartilhados dentro do module

## Erros comuns

| Erro | Correção |
| --- | --- |
| `styles["tag-promo"]` | camelCase no objeto ou colchetes com kebab-case |
| Classe de outro componente | `styles` só vê o próprio arquivo |
| `className="card"` sem `styles.` | Global — o module não aplica |
| `import "./Card.module.css"` sem variável | Funciona, mas você não pode usar as classes |
