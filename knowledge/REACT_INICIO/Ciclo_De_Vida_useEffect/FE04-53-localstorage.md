# FE04-53 — localStorage

## O que é o localStorage

Armazenamento do navegador que persiste **entre sessões** — fecha a aba, reinicia o PC, e os dados continuam. Armazena **apenas strings**, com chave e valor.

```javascript
localStorage.setItem("tema", "escuro");    // salva
localStorage.getItem("tema");              // "escuro"
localStorage.removeItem("tema");           // remove uma chave
localStorage.clear();                      // limpa tudo
```

## Revisão dos limites

| Característica | Detalhe |
| --- | --- |
| Persistência | Permanente até ser apagado |
| Capacidade | ~5-10 MB por domínio |
| Tipos | **Somente strings** — objetos precisam de `JSON.stringify` |
| Escopo | Por domínio (`site.com` não vê `outro.com`) |
| Sync | Síncrono — bloqueia se abusado |

## O padrão React + localStorage

### Salvar quando o estado muda

```jsx
const [tema, setTema] = useState("claro");

useEffect(() => {
  localStorage.setItem("tema", tema);
}, [tema]); // salva toda vez que tema muda
```

### Ler na inicialização

**Opção A — dentro do useEffect:**

```jsx
const [tema, setTema] = useState("claro");

useEffect(() => {
  const salvo = localStorage.getItem("tema");
  if (salvo) setTema(salvo);
}, []);
```

**Opção B — lazy initializer (melhor):**

```jsx
const [tema, setTema] = useState(() => {
  return localStorage.getItem("tema") || "claro";
});
```

A função de inicialização roda **uma única vez** — o React usa o retorno como valor inicial. Mais limpo, sem efeito separado.

## Objetos e arrays — sempre via JSON

```jsx
const [favoritos, setFavoritos] = useState(() => {
  const salvo = localStorage.getItem("favoritos");
  return salvo ? JSON.parse(salvo) : [];
});

useEffect(() => {
  localStorage.setItem("favoritos", JSON.stringify(favoritos));
}, [favoritos]);
```

## O erro mais comum — JSON.parse sem proteção

```jsx
// ❌ quebra se o dado estiver corrompido
const [dados] = useState(() => JSON.parse(localStorage.getItem("dados")));

// ✅ protegido
const [dados] = useState(() => {
  try {
    const salvo = localStorage.getItem("dados");
    return salvo ? JSON.parse(salvo) : [];
  } catch {
    return []; // fallback se o JSON estiver corrompido
  }
});
```

## Caso completo — tema persistente

```jsx
function App() {
  const [tema, setTema] = useState(() => {
    try {
      return localStorage.getItem("tema") || "claro";
    } catch {
      return "claro";
    }
  });

  // Salva toda vez que muda
  useEffect(() => {
    localStorage.setItem("tema", tema);
  }, [tema]);

  // Aplica no DOM
  useEffect(() => {
    document.documentElement.dataset.tema = tema;
  }, [tema]);

  return (
    <button onClick={() => setTema(t => t === "claro" ? "escuro" : "claro")}>
      Tema: {tema}
    </button>
  );
}
```

```css
:root[data-tema="escuro"] {
  --fundo: #1a1a1a;
  --texto: #fff;
}
```

## Os dois momentos — leitura vs escrita

| Momento | Como | Quando |
| --- | --- | --- |
| **Ler** | `useState(() => getItem())` | Inicialização — lazy init |
| **Escrever** | `useEffect(() => setItem())` | Toda vez que o estado muda |

## Alternativas

| Storage | Quando usar |
| --- | --- |
| `localStorage` | Preferências, cache — persiste |
| `sessionStorage` | Dados por aba — morre ao fechar |
| Cookies | Só quando o servidor precisa ler |
| IndexedDB | Grandes volumes, dados estruturados |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `setItem` com objeto direto | Vira `"[object Object]"` — use `JSON.stringify` |
| `JSON.parse` sem try/catch | Quebra com dados corrompidos |
| Ler a cada render | `useState(() => getItem())` — lazy init |
| Salvar dados sensíveis | localStorage é legível por qualquer script — nada de senhas/tokens |
| Chave sem prefixo | Use `meuapp:tema` para evitar colisões |

## Resumo

- localStorage persiste strings entre sessões — objetos via `JSON.stringify`/`parse`
- React lê na inicialização (`useState` com função lazy) e escreve no `useEffect`
- `try/catch` no `JSON.parse` protege de dados corrompidos
- Não salve dados sensíveis — qualquer script lê o storage
