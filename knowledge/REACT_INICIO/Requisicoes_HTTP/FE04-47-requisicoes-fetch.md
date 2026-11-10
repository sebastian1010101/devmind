# FE04-47 — Requisições: Fetch

## A API fetch

`fetch` é a API nativa do navegador para requisições HTTP — retorna uma `Promise` que resolve num objeto `Response`.

```javascript
const resposta = await fetch("https://api.exemplo.com/produtos");
const dados = await resposta.json();
```

## GET — buscando dados

```javascript
async function buscarProdutos() {
  const res = await fetch("https://fakestoreapi.com/products");

  if (!res.ok) {
    throw new Error(`Erro ${res.status}`);
  }

  return await res.json();
}
```

⚠️ `fetch` **não lança erro em 404/500** — `res.ok` é `false`, mas a Promise resolve. Sempre cheque `res.ok`.

## POST — enviando dados

```javascript
async function criarUsuario(usuario) {
  const res = await fetch("/api/usuarios", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(usuario)
  });

  if (!res.ok) throw new Error(`Erro ${res.status}`);
  return await res.json();
}
```

## PUT/PATCH — atualizando

```javascript
await fetch(`/api/usuarios/${id}`, {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nome: "Novo Nome" })
});
```

## DELETE — removendo

```javascript
await fetch(`/api/usuarios/${id}`, {
  method: "DELETE"
});
```

## Headers essenciais

```javascript
headers: {
  "Content-Type": "application/json",     // tipo do body enviado
  "Authorization": `Bearer ${token}`,     // autenticação
  "Accept": "application/json"            // tipo esperado na resposta
}
```

## O objeto Response

```javascript
const res = await fetch(url);

res.status        // 200, 404, 500...
res.ok            // true se status 200-299
res.headers       // Headers da resposta
await res.json()  // parseia o body como JSON
await res.text()  // body como texto
```

## O padrão completo no React

```jsx
function ListaProdutos() {
  const [produtos, setProdutos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    async function carregar() {
      try {
        const res = await fetch("https://fakestoreapi.com/products");
        if (!res.ok) throw new Error("Falha ao carregar");
        const dados = await res.json();
        setProdutos(dados);
      } catch (e) {
        setErro(e.message);
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, []);

  if (carregando) return <p>Carregando...</p>;
  if (erro) return <p>Erro: {erro}</p>;

  return (
    <ul>
      {produtos.map(p => <li key={p.id}>{p.title}</li>)}
    </ul>
  );
}
```

O tripé `dados + carregando + erro` é o padrão de toda requisição assíncrona.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `fetch` sem `res.ok` | 404 resolve normalmente — cheque manualmente |
| `res.json()` sem `await` | Retorna Promise — precisa de await |
| `body: objeto` sem stringify | `JSON.stringify(obj)` + header Content-Type |
| Sem try/catch | Erros de rede/rede offline quebram silenciosamente |
| Fetch no corpo do componente | `useEffect` — senão dispara a cada render |

## Resumo

- `fetch` retorna `Promise<Response>` — `await res.json()` para os dados
- `res.ok` é manual — `fetch` não falha em 404/500
- `method`, `headers` e `body: JSON.stringify()` para POST/PUT/PATCH
- O padrão `useState` para dados/loading/erro é obrigatório em requisições React
