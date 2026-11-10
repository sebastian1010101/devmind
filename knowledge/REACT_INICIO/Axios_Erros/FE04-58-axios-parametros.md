# FE04-58 — Lidando com parâmetros no Axios

## Os três tipos de parâmetro

```text
URL dinâmica    →  /api/produtos/42          (path param)
Query string    →  /api/produtos?categoria=eletronicos&page=2
Body            →  POST { nome: "Ana" }       (dados do corpo)
```

## Path params — URL dinâmica

```javascript
// Variável na URL — use template literals
const res = await api.get(`/produtos/${id}`);

// Com axios.create e URL base
await api.get(`/usuarios/${userId}/posts/${postId}`);
```

## Query params — filtro e paginação

```javascript
// Forma manual — na URL
await api.get("/produtos?categoria=eletronicos&limite=10");

// Forma recomendada — objeto params
const res = await api.get("/produtos", {
  params: {
    categoria: "eletronicos",
    limite: 10,
    pagina: 2
  }
});
// axios monta: /produtos?categoria=eletronicos&limite=10&pagina=2
```

Vantagens do objeto `params`:

- Serialização automática (inclusive arrays)
- Encoding de caracteres especiais
- Limpo e legível

```javascript
// Arrays viram múltiplos params
await api.get("/produtos", {
  params: { tags: ["oferta", "novo"] }
});
// → /produtos?tags[]=oferta&tags[]=novo (depende da API)
```

## Body — dados do POST/PUT/PATCH

```javascript
// O segundo argumento do post é o body
await api.post("/usuarios", {
  nome: "Ana",
  email: "ana@email.com",
  idade: 28
});
```

```javascript
await api.put(`/usuarios/${id}`, usuarioCompleto);
await api.patch(`/usuarios/${id}`, { nome: "Só o nome" });
```

## Combinando — path + query + body

```javascript
// PATCH num recurso com filtro de contexto
await api.patch(
  `/projetos/${projetoId}/tarefas/${tarefaId}`,
  { status: "concluida" },           // body
  { params: { notificar: true } }    // query string
);
// → PATCH /projetos/1/tarefas/5?notificar=true
//   body: { status: "concluida" }
```

## Headers personalizados

```javascript
await api.get("/dados", {
  headers: {
    Authorization: `Bearer ${token}`,
    "X-Custom": "valor"
  },
  params: { page: 1 }
});
```

## Busca com parâmetros — exemplo React

```jsx
function Busca() {
  const [termo, setTermo] = useState("");
  const [resultados, setResultados] = useState([]);

  async function buscar() {
    const res = await api.get("/produtos", {
      params: {
        q: termo,
        categoria: categoriaSelecionada,
        ordenar: ordenacao
      }
    });
    setResultados(res.data);
  }

  // ...form chama buscar()
}
```

## Paginação

```jsx
const [pagina, setPagina] = useState(1);

useEffect(() => {
  async function carregar() {
    const res = await api.get("/produtos", {
      params: { _page: pagina, _limit: 10 }
    });
    setProdutos(res.data);
  }
  carregar();
}, [pagina]); // recarrega ao mudar de página
```

## Interceptor de params — lógica global

```javascript
// Adiciona um parâmetro em TODA requisição
api.interceptors.request.use(config => {
  config.params = {
    ...config.params,
    api_key: "sua-chave",
    lang: "pt-BR"
  };
  return config;
});
```

## paramsSerializer — formatos customizados

Algumas APIs esperam formato específico:

```javascript
await api.get("/produtos", {
  params: { ids: [1, 2, 3] },
  paramsSerializer: params =>
    `ids=${params.ids.join(",")}` // → ids=1,2,3
});
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Query na URL manual com `+` | `params` — axios cuida do encoding |
| `POST` passando params no lugar errado | `api.post(url, body, { params })` — body é 2º arg |
| Esquecer deps no `useEffect` | Liste `pagina`, `filtro` — tudo que dispara o efeito |
| Params sensíveis na URL | Query params ficam no histórico — dados sensíveis vão no body |

## Resumo

- Path: `api.get(\`/recurso/${id}\`)` — URL dinâmica
- Query: `params: { ... }` — serialização automática e encoding
- Body: segundo argumento do `post`/`put`/`patch`
- Combine os três livremente — axios separa cada um no lugar certo
