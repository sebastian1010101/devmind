# FE04-60 — Atividade: Refatorando atividades com try-catch

## Objetivo

Pegar as atividades anteriores (notícias, ViaCEP) e refatorar com `try/catch` completo, `axios`, instância configurada e tratamento de erros tipado.

## Antes — o código básico

```jsx
useEffect(() => {
  fetch("https://jsonplaceholder.typicode.com/posts")
    .then(r => r.json())
    .then(setNoticias);
}, []); // sem tratamento, sem loading, sem erro
```

## Depois — refatorado

### 1. Instância do axios

```javascript
// src/services/api.js
import axios from "axios";

export const api = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  timeout: 8000
});
```

### 2. Hook customizado (opcional — mas limpa o componente)

```javascript
// src/hooks/useFetch.js
import { useState, useEffect } from "react";
import { api } from "../services/api";

export function useFetch(url) {
  const [dados, setDados] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    async function carregar() {
      setCarregando(true);
      setErro(null);

      try {
        const res = await api.get(url);
        setDados(res.data);
      } catch (e) {
        setErro(traduzirErro(e));
      } finally {
        setCarregando(false);
      }
    }
    carregar();
  }, [url]);

  return { dados, carregando, erro };
}

function traduzirErro(e) {
  if (e.code === "ECONNABORTED") return "Tempo esgotado";
  if (e.code === "ERR_NETWORK") return "Sem conexão";
  if (e.response?.status === 404) return "Não encontrado";
  if (e.response?.status >= 500) return "Servidor indisponível";
  return e.message;
}
```

### 3. O componente limpo

```jsx
import { useFetch } from "./hooks/useFetch";

function ListaNoticias() {
  const { dados: noticias, carregando, erro } = useFetch("/posts?_limit=10");

  if (carregando) return <p>Carregando...</p>;
  if (erro) return <p>Erro: {erro}</p>;

  return (
    <ul>
      {noticias.map(n => <li key={n.id}>{n.title}</li>)}
    </ul>
  );
}
```

## Refatorando o ViaCEP

### Antes

```jsx
// fetch manual, res.ok, dados.erro, try/catch improvisado
```

### Depois

```javascript
// src/services/viacep.js
import axios from "axios";

export const viacep = axios.create({
  baseURL: "https://viacep.com.br/ws",
  timeout: 8000
});
```

```jsx
import { viacep } from "./services/viacep";

useEffect(() => {
  if (!cepBusca) return;

  async function buscar() {
    setCarregando(true);
    setErro(null);

    try {
      const res = await viacep.get(`/${cepBusca}/json/`);

      if (res.data.erro) {
        throw new Error("CEP não encontrado");
      }

      setEndereco(res.data);
    } catch (e) {
      setErro(e.response?.status === 404 
        ? "CEP não encontrado"
        : e.message || "Erro na busca");
      setEndereco(null);
    } finally {
      setCarregando(false);
    }
  }

  buscar();
}, [cepBusca]);
```

## O checklist de refatoração

| Antes | Depois |
| --- | --- |
| `fetch(url)` | `api.get(url)` com instância |
| `res.ok` manual | Axios lança automaticamente |
| `res.json()` | `res.data` |
| URL completa | `baseURL` centralizada |
| Erro genérico | Mensagens tipadas por status |
| Loading ausente | `carregando` com `finally` |
| Try/catch improvisado | `try/catch/finally` consistente |

## Desafios extras

### Desafio A — retry automático

```javascript
useEffect(() => {
  let cancelado = false;

  async function carregar(tentativas = 3) {
    for (let i = 0; i < tentativas; i++) {
      try {
        const res = await api.get(url);
        if (!cancelado) setDados(res.data);
        return;
      } catch (e) {
        if (i === tentativas - 1) {
          if (!cancelado) setErro(traduzirErro(e));
        } else {
          await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        }
      }
    }
  }

  carregar();
  return () => { cancelado = true; };
}, [url]);
```

### Desafio B — toast de erro

```jsx
import { ToastContainer, toast } from "react-toastify";

catch (e) {
  toast.error(traduzirErro(e)); // notificação flutuante
}
```

### Desafio C — skeleton + retry button

```jsx
if (carregando) {
  return <div className="skeleton" />;
}

if (erro) {
  return (
    <div className="erro">
      <p>{erro}</p>
      <button onClick={() => setAtualizar(a => a + 1)}>
        Tentar novamente
      </button>
    </div>
  );
}
```

## Critérios de verificação

- `axios.create` com `baseURL` e `timeout`
- `try/catch/finally` em todas as requisições
- Mensagens de erro traduzidas por tipo
- `res.data` em vez de `res.json()`
- Loading sempre desliga no `finally`
- Hook customizado extrai lógica repetida

## Erros comuns na refatoração

| Erro | Correção |
| --- | --- |
| `res.json()` no axios | `res.data` — já é objeto |
| `res.ok` no axios | Não existe — axios lança em status ≠ 2xx |
| `api.get` sem baseURL | Configure `axios.create` uma vez |
| Try/catch só no fetch | Coloque em **todas** as requisições |
| Loading fora do `finally` | Pode nunca desligar em erro |
