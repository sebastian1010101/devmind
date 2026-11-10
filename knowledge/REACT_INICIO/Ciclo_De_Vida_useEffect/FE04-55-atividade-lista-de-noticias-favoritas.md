# FE04-55 — Atividade: Lista de notícias favoritas

## Objetivo

Combinar tudo: `useEffect` de montagem (fetch), `useEffect` de atualização (salvar favoritos), e `localStorage` para persistir.

## O cenário

App de notícias onde o usuário marca artigos como favoritos — os favoritos sobrevivem ao recarregar a página.

## A implementação

```jsx
import { useState, useEffect } from "react";

function ListaNoticias() {
  const [noticias, setNoticias] = useState([]);
  const [favoritos, setFavoritos] = useState(() => {
    try {
      const salvo = localStorage.getItem("favoritos");
      return salvo ? JSON.parse(salvo) : [];
    } catch {
      return [];
    }
  });
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  // Montagem: busca as notícias uma vez
  useEffect(() => {
    async function carregar() {
      try {
        const res = await fetch(
          "https://jsonplaceholder.typicode.com/posts?_limit=20"
        );
        if (!res.ok) throw new Error(`Erro ${res.status}`);
        setNoticias(await res.json());
      } catch (e) {
        setErro(e.message);
      } finally {
        setCarregando(false);
      }
    }
    carregar();
  }, []);

  // Atualização: salva favoritos a cada mudança
  useEffect(() => {
    localStorage.setItem("favoritos", JSON.stringify(favoritos));
  }, [favoritos]);

  function alternarFavorito(id) {
    setFavoritos(atual =>
      atual.includes(id)
        ? atual.filter(f => f !== id)   // remove
        : [...atual, id]                 // adiciona
    );
  }

  if (carregando) return <p>Carregando...</p>;
  if (erro) return <p>Erro: {erro}</p>;

  return (
    <div>
      <h1>Notícias</h1>
      <p>{favoritos.length} favoritas</p>
      <ul>
        {noticias.map(n => (
          <li key={n.id}>
            <h3>{n.title}</h3>
            <p>{n.body}</p>
            <button onClick={() => alternarFavorito(n.id)}>
              {favoritos.includes(n.id) ? "★ Favorita" : "☆ Favoritar"}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## O fluxo de dados

```text
Montagem:
  fetch → setNoticias → renderiza lista
  lazy init → lê favoritos do localStorage

Clique em favoritar:
  alternarFavorito → setFavoritos → re-render
  useEffect [favoritos] → localStorage.setItem

Reload:
  lazy init → lê os IDs salvos
  noticias chegam do fetch → estrelas aparecem
```

## Variação — favoritos como objetos completos

Guardar só IDs funciona se a lista sempre vem da mesma API. Para favoritar de fontes diferentes, guarde o objeto:

```jsx
function alternarFavorito(noticia) {
  setFavoritos(atual =>
    atual.some(f => f.id === noticia.id)
      ? atual.filter(f => f.id !== noticia.id)
      : [...atual, noticia]
  );
}
```

## Desafios extras

### Desafio A — aba de favoritos

```jsx
const [mostrarFavoritos, setMostrarFavoritos] = useState(false);

const exibidas = mostrarFavoritos
  ? noticias.filter(n => favoritos.includes(n.id))
  : noticias;
```

### Desafio B — contador no título

```jsx
useEffect(() => {
  document.title = favoritos.length > 0
    ? `(${favoritos.length}) Notícias`
    : "Notícias";
}, [favoritos]);
```

### Desafio C — animação de entrada

```jsx
// CSS
.noticia {
  animation: entrar 0.3s ease-out;
}
@keyframes entrar {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

## Os dois useEffects — a separação de responsabilidades

```jsx
// Efeito 1: fetch (montagem)
useEffect(() => {
  carregar();
}, []);

// Efeito 2: persistência (atualização de favoritos)
useEffect(() => {
  localStorage.setItem("favoritos", JSON.stringify(favoritos));
}, [favoritos]);
```

**Não misture** — um efeito para cada responsabilidade. Fica mais fácil de debugar e cada um tem suas deps certas.

## Critérios de verificação

- Fetch com `[]` na montagem
- Favoritos com lazy init + `try/catch`
- `setItem` no `useEffect` com `[favoritos]`
- `alternarFavorito` usa forma funcional `setFavoritos(atual => ...)`
- `key={n.id}` e estrelas indicando estado
- Reload preserva os favoritos

## Erros comuns

| Erro | Correção |
| --- | --- |
| `JSON.parse` sem try/catch | Proteja — storage pode estar corrompido |
| `setFavoritos([...favoritos, id])` | Forma funcional `setFavoritos(atual => ...)` — evita estado velho |
| Favoritar mas não persistir | `useEffect` com `[favoritos]` — não chame setItem no clique |
| Mesmo effect para fetch e storage | Dois `useEffect` separados — um por responsabilidade |
