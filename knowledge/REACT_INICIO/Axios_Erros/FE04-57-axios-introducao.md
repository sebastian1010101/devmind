# FE04-57 — Axios: Introdução

## O que é o Axios

Biblioteca HTTP para JavaScript — uma alternativa ao `fetch` com sintaxe mais enxuta e recursos extras embutidos.

```bash
npm install axios
```

```javascript
import axios from "axios";

const res = await axios.get("https://api.exemplo.com/produtos");
console.log(res.data); // dados já parseados — sem .json()
```

## Axios vs fetch — as diferenças

| `fetch` | `axios` |
| --- | --- |
| Nativo do navegador | Precisa instalar |
| `res.json()` manual | `res.data` automático |
| Não falha em 404/500 | Lança erro em qualquer status ≠ 2xx |
| `JSON.stringify` + headers manuais | Serializa objetos automaticamente |
| Sem timeout nativo | `timeout` embutido |
| Sem progresso de upload | `onUploadProgress` |
| Cancelamento manual (AbortController) | AbortController ou CancelToken |

## O verbo GET

```javascript
// Simples
const res = await axios.get("/api/usuarios");
console.log(res.data); // array de usuários

// Com headers
const res = await axios.get("/api/usuarios", {
  headers: { Authorization: `Bearer ${token}` }
});
```

## POST — criando dados

```javascript
const res = await axios.post("/api/usuarios", {
  nome: "Ana",
  email: "ana@email.com"
});
// body é objeto — axios serializa e adiciona Content-Type
```

## PUT/PATCH — atualizando

```javascript
await axios.put(`/api/usuarios/${id}`, usuarioCompleto);
await axios.patch(`/api/usuarios/${id}`, { nome: "Novo" });
```

## DELETE — removendo

```javascript
await axios.delete(`/api/usuarios/${id}`);
```

## A instância configurada — api.js

Centralizar a URL base e headers evita repetir em toda chamada:

```javascript
// src/services/api.js
import axios from "axios";

export const api = axios.create({
  baseURL: "https://api.exemplo.com",
  timeout: 8000, // 8 segundos
  headers: {
    "Content-Type": "application/json"
  }
});
```

```javascript
// em qualquer componente
import { api } from "./services/api";

const res = await api.get("/produtos"); // baseURL + /produtos
```

## O objeto de resposta

```javascript
const res = await axios.get("/api/produtos");

res.data      // body parseado — o que você quer
res.status    // 200, 201, 404...
res.headers   // headers da resposta
res.config    // configuração usada na requisição
res.request   // objeto da requisição
```

## Interceptors — middleware de requisição

Código que roda **antes de cada requisição** ou **depois de cada resposta**:

```javascript
// Adiciona token em toda requisição
api.interceptors.request.use(config => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Trata 401 globalmente — redireciona pro login
api.interceptors.response.use(
  res => res,
  erro => {
    if (erro.response?.status === 401) {
      window.location.href = "/login";
    }
    return Promise.reject(erro);
  }
);
```

## No React — o padrão

```jsx
import { api } from "./services/api";

useEffect(() => {
  async function carregar() {
    try {
      const res = await api.get("/produtos");
      setProdutos(res.data); // dados direto — sem .json()
    } catch (e) {
      setErro(e.response?.data?.message || e.message);
    } finally {
      setCarregando(false);
    }
  }
  carregar();
}, []);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `res.json()` no axios | `res.data` — já é objeto |
| `body: JSON.stringify()` | `axios.post(url, obj)` — serializa sozinho |
| `res.ok` no axios | Não existe — axios lança erro em status ≠ 2xx |
| URL completa em toda chamada | `axios.create({ baseURL })` |

## Resumo

- Axios encurta requisições: `res.data` direto, erro em status ≠ 2xx, serialização automática
- `axios.create({ baseURL })` centraliza configuração
- Interceptors adicionam lógica global (token, redirect 401)
- No React: mesmo padrão do `useEffect`, sintaxe mais limpa
