# FE04-48 — Atividade: Trazendo uma lista de notícias via API

## Objetivo

Fazer uma requisição `fetch` real, gerenciar os três estados (dados/loading/erro) e renderizar a lista retornada.

## API de exemplo

Usaremos a [JSONPlaceholder](https://jsonplaceholder.typicode.com) — API fake gratuita:

```text
GET https://jsonplaceholder.typicode.com/posts
→ retorna 100 posts { id, title, body, userId }
```

## A implementação

```jsx
import { useState, useEffect } from "react";

function ListaNoticias() {
  const [noticias, setNoticias] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    async function carregar() {
      try {
        const res = await fetch(
          "https://jsonplaceholder.typicode.com/posts?_limit=10"
        );

        if (!res.ok) {
          throw new Error(`Erro ${res.status}: ${res.statusText}`);
        }

        const dados = await res.json();
        setNoticias(dados);
      } catch (e) {
        setErro(e.message);
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, []); // [] = roda uma vez, na montagem

  if (carregando) {
    return <p>Carregando notícias...</p>;
  }

  if (erro) {
    return (
      <div className="erro">
        <p>❌ {erro}</p>
        <button onClick={() => window.location.reload()}>Tentar novamente</button>
      </div>
    );
  }

  return (
    <div>
      <h1>Últimas notícias</h1>
      <ul>
        {noticias.map(n => (
          <li key={n.id}>
            <h3>{n.title}</h3>
            <p>{n.body}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ListaNoticias;
```

## Componente separado para o item

```jsx
// components/Noticia.jsx
function Noticia({ titulo, corpo }) {
  return (
    <article className="noticia">
      <h3>{titulo}</h3>
      <p>{corpo}</p>
    </article>
  );
}
```

```jsx
{noticias.map(n => (
  <Noticia key={n.id} titulo={n.title} corpo={n.body} />
))}
```

## Desafios extras

### Desafio A — botão de recarregar

```jsx
const [atualizar, setAtualizar] = useState(0);

useEffect(() => {
  carregar();
}, [atualizar]); // re-executa quando 'atualizar' muda

<button onClick={() => setAtualizar(a => a + 1)}>Atualizar</button>
```

### Desafio B — busca por ID

```jsx
const [idBusca, setIdBusca] = useState("");

async function buscarPorId() {
  const res = await fetch(
    `https://jsonplaceholder.typicode.com/posts/${idBusca}`
  );
  const dados = await res.json();
  setNoticias([dados]); // array com um item
}
```

### Desafio C — skeleton loading

```jsx
if (carregando) {
  return (
    <div>
      {[1,2,3].map(i => (
        <div key={i} className="skeleton" />
      ))}
    </div>
  );
}
```

## O tripé de estados — visualizado

| `carregando` | `erro` | `noticias` | O que mostra |
| --- | --- | --- | --- |
| true | null | [] | Spinner/skeleton |
| false | msg | [] | Mensagem de erro |
| false | null | [dados] | Lista renderizada |
| false | null | [] | "Nenhuma notícia" |

## Critérios de verificação

- `useEffect` com `[]` — requisição só na montagem
- `res.ok` checado antes de `.json()`
- `try/catch/finally` — erro tratado, loading sempre desligado
- `key={n.id}` na lista
- Três estados visuais cobertos: loading, erro, dados

## Erros comuns

| Erro | Correção |
| --- | --- |
| Fetch sem `useEffect` | Roda a cada render — loop de requisições |
| `async` direto no `useEffect` | `useEffect(async () => ...)` é proibido — declare a função dentro |
| Sem `res.ok` | 404 cai no `then` como se fosse sucesso |
| Loading nunca desliga | `setCarregando(false)` no `finally` |
