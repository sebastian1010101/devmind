# FE04-65 — Hooks customizados

## O que é um hook customizado

Uma **função que usa outros hooks** para reutilizar lógica de estado entre componentes. Começa com `use`, pode usar `useState`, `useEffect`, `useRef` — qualquer hook.

```jsx
function useContador() {
  const [contador, setContador] = useState(0);

  const incrementar = () => setContador(c => c + 1);
  const decrementar = () => setContador(c => c - 1);
  const resetar = () => setContador(0);

  return { contador, incrementar, decrementar, resetar };
}
```

```jsx
function App() {
  const { contador, incrementar } = useContador();
  // toda lógica do contador, reusável em qualquer lugar
}
```

## As regras

1. Nome começa com `use` — obrigatório
2. Pode chamar outros hooks dentro
3. Retorna o que quiser: valor, objeto, array
4. Cada chamada tem estado **independente** — não compartilhado

## Os casos clássicos

### useLocalStorage — estado persistente

```jsx
function useLocalStorage(chave, valorInicial) {
  const [valor, setValor] = useState(() => {
    try {
      const salvo = localStorage.getItem(chave);
      return salvo ? JSON.parse(salvo) : valorInicial;
    } catch {
      return valorInicial;
    }
  });

  useEffect(() => {
    localStorage.setItem(chave, JSON.stringify(valor));
  }, [chave, valor]);

  return [valor, setValor]; // mesma API do useState
}
```

```jsx
const [tema, setTema] = useLocalStorage("tema", "claro");
// mesma sintaxe do useState — mas persiste!
```

### useFetch — requisição genérica

```jsx
function useFetch(url) {
  const [dados, setDados] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function carregar() {
      setCarregando(true);
      setErro(null);
      try {
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) throw new Error(`Erro ${res.status}`);
        setDados(await res.json());
      } catch (e) {
        if (e.name !== "AbortError") setErro(e.message);
      } finally {
        setCarregando(false);
      }
    }
    carregar();

    return () => controller.abort();
  }, [url]);

  return { dados, carregando, erro };
}
```

```jsx
const { dados: usuarios, carregando } = useFetch("/api/usuarios");
```

### useToggle — booleano com helpers

```jsx
function useToggle(inicial = false) {
  const [valor, setValor] = useState(inicial);

  const alternar = () => setValor(v => !v);
  const ligar = () => setValor(true);
  const desligar = () => setValor(false);

  return [valor, { alternar, ligar, desligar }];
}
```

```jsx
const [aberto, { alternar, desligar }] = useToggle();
<button onClick={alternar}>Toggle</button>
<Modal aberto={aberto} fechar={desligar} />
```

### useDebounce — atrasar um valor

```jsx
function useDebounce(valor, delay = 500) {
  const [debounced, setDebounced] = useState(valor);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(valor), delay);
    return () => clearTimeout(timer);
  }, [valor, delay]);

  return debounced;
}
```

```jsx
const [busca, setBusca] = useState("");
const buscaDebounced = useDebounce(busca, 500);

useEffect(() => {
  if (buscaDebounced) fetch(`/api/busca?q=${buscaDebounced}`)...
}, [buscaDebounced]); // só busca depois de 500ms sem digitar
```

### useWindowSize — dimensões da tela

```jsx
function useWindowSize() {
  const [size, setSize] = useState({
    largura: window.innerWidth,
    altura: window.innerHeight
  });

  useEffect(() => {
    function aoResize() {
      setSize({ largura: innerWidth, altura: innerHeight });
    }
    window.addEventListener("resize", aoResize);
    return () => window.removeEventListener("resize", aoResize);
  }, []);

  return size;
}
```

## Componente antes vs depois

```jsx
// ❌ ANTES — lógica misturada na UI
function Lista() {
  const [dados, setDados] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    // 20 linhas de fetch, erro, loading...
  }, []);

  // render...
}

// ✅ DEPOIS — lógica extraída
function Lista() {
  const { dados, carregando, erro } = useFetch("/api/produtos");

  // render limpo, focado na UI
}
```

## Compartilhamento — o estado NÃO é compartilhado

```jsx
function A() { const c = useContador(); } // contador próprio
function B() { const c = useContador(); } // outro contador, independente
```

Cada chamada de hook customizado cria estado separado. Para estado global, use Context ou Zustand/Redux.

## Organização

```text
src/
├── hooks/
│   ├── useFetch.js
│   ├── useLocalStorage.js
│   ├── useToggle.js
│   └── useDebounce.js
├── components/
└── services/
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Nome sem `use` | O React não reconhece como hook — renomeie |
| Hook dentro de condição | Mesmas regras do `useState` — sempre no topo |
| Retornar JSX | Hooks retornam dados/lógica — JSX é do componente |
| Estado compartilhado esperado | Cada chamada é independente — use Context se precisar global |

## Resumo

- Hook customizado = função `use*` que encapsula lógica com outros hooks
- Reutiliza estado/efeitos entre componentes — UI limpa
- Casos: `useFetch`, `useLocalStorage`, `useToggle`, `useDebounce`
- Estado é independente por chamada — não é global
