# FE04-41 — Passo a Passo: The Books

## O projeto

Catálogo de livros — exercício integrador de listas, condicionais, estado e componentes: listagem com filtro, favoritos e visual condicional.

## Estrutura

```text
src/
├── components/
│   ├── Header/
│   ├── BookCard/
│   ├── BookList/
│   └── FilterBar/
├── data/
│   └── livros.js
└── App.jsx
```

## Os dados

```javascript
// src/data/livros.js
export const livros = [
  { id: 1, titulo: "O Nome do Vento", autor: "Patrick Rothfuss", genero: "fantasia", paginas: 662 },
  { id: 2, titulo: "Clean Code", autor: "Robert Martin", genero: "tecnico", paginas: 464 },
  { id: 3, titulo: "Duna", autor: "Frank Herbert", genero: "ficcao", paginas: 688 },
  { id: 4, titulo: "1984", autor: "George Orwell", genero: "ficcao", paginas: 328 }
];
```

## Estado no App

```jsx
import { useState } from "react";
import { livros } from "./data/livros";
import BookList from "./components/BookList/BookList";
import FilterBar from "./components/FilterBar/FilterBar";

function App() {
  const [favoritos, setFavoritos] = useState([]);
  const [filtro, setFiltro] = useState("todos");

  function toggleFavorito(id) {
    setFavoritos(prev =>
      prev.includes(id)
        ? prev.filter(f => f !== id)
        : [...prev, id]
    );
  }

  const exibidos = filtro === "todos"
    ? livros
    : livros.filter(l => l.genero === filtro);

  return (
    <>
      <FilterBar filtro={filtro} onChange={setFiltro} />
      <BookList
        livros={exibidos}
        favoritos={favoritos}
        onFavoritar={toggleFavorito}
      />
    </>
  );
}
```

## FilterBar — controle de filtro

```jsx
const GENEROS = ["todos", "fantasia", "ficcao", "tecnico"];

function FilterBar({ filtro, onChange }) {
  return (
    <div className="filter-bar">
      {GENEROS.map(g => (
        <button
          key={g}
          className={filtro === g ? "ativo" : ""}
          onClick={() => onChange(g)}
        >
          {g}
        </button>
      ))}
    </div>
  );
}
```

## BookCard — visual condicional

```jsx
function BookCard({ livro, favorito, onFavoritar }) {
  return (
    <article className={`book-card ${favorito ? "favorito" : ""}`}>
      <h3>{livro.titulo}</h3>
      <p>{livro.autor}</p>
      <span className="genero">{livro.genero}</span>
      <p>{livro.paginas} páginas</p>

      <button
        className={favorito ? "btn-fav ativo" : "btn-fav"}
        onClick={() => onFavoritar(livro.id)}
      >
        {favorito ? "❤️" : "🤍"}
      </button>
    </article>
  );
}
```

## BookList — o vazio tratado

```jsx
function BookList({ livros, favoritos, onFavoritar }) {
  if (livros.length === 0) {
    return <p className="vazio">Nenhum livro encontrado neste gênero.</p>;
  }

  return (
    <div className="book-grid">
      {livros.map(livro => (
        <BookCard
          key={livro.id}
          livro={livro}
          favorito={favoritos.includes(livro.id)}
          onFavoritar={onFavoritar}
        />
      ))}
    </div>
  );
}
```

## Lições do exercício

| Conceito | Onde aparece |
| --- | --- |
| Lista + key | `livros.map` com `key={livro.id}` |
| Condicional | `{favorito ? "❤️" : "🤍"}` e classe `favorito` |
| Estado compartilhado | `favoritos` no App, passado por props |
| Derivação | `exibidos` calculado de `filtro` + `livros` |
| Toggle em array | `includes` + `filter`/`spread` |
| Estado vazio | `livros.length === 0` antes do map |

## Extensões

- Busca por título com input controlado
- Contador de favoritos no Header
- `localStorage` para persistir favoritos (visto no módulo 3)
- Ordenação por páginas/título
