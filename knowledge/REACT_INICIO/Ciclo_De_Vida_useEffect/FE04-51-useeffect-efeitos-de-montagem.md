# FE04-51 — useEffect: Efeitos de montagem

## O que é um efeito de montagem

Um efeito que roda **uma única vez** — quando o componente aparece pela primeira vez no DOM. É o `useEffect` com array de dependências **vazio**:

```jsx
useEffect(() => {
  console.log("Montou!");
}, []); // ← [] = nunca mais roda (até desmontar e remontar)
```

## Os casos de uso clássicos

### 1. Requisição inicial de dados

```jsx
function Produtos() {
  const [produtos, setProdutos] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregar() {
      const res = await fetch("/api/produtos");
      const dados = await res.json();
      setProdutos(dados);
      setCarregando(false);
    }

    carregar();
  }, []); // busca uma vez ao montar

  if (carregando) return <p>Carregando...</p>;
  return <ul>{produtos.map(p => <li key={p.id}>{p.nome}</li>)}</ul>;
}
```

### 2. Ler localStorage na inicialização

```jsx
function App() {
  const [tema, setTema] = useState("claro");

  useEffect(() => {
    const salvo = localStorage.getItem("tema");
    if (salvo) setTema(salvo);
  }, []); // lê uma vez — depois o estado manda
```

Ou com inicialização lazy (melhor — evita o efeito):

```jsx
const [tema, setTema] = useState(() =>
  localStorage.getItem("tema") || "claro"
);
```

### 3. Configurar listeners globais

```jsx
useEffect(() => {
  function aoRedimensionar() {
    setLargura(window.innerWidth);
  }

  window.addEventListener("resize", aoRedimensionar);

  return () => {
    window.removeEventListener("resize", aoRedimensionar);
  };
}, []); // adiciona na montagem, remove na desmontagem
```

### 4. Inicializar bibliotecas externas

```jsx
useEffect(() => {
  const mapa = new GoogleMap(ref.current, { zoom: 10 });
  // inicializa uma vez — o mapa vive fora do React

  return () => mapa.destroy();
}, []);
```

### 5. Focar num input na entrada

```jsx
useEffect(() => {
  inputRef.current.focus();
}, []); // cursor no campo assim que a tela abre
```

## A timeline de montagem

```text
1. Componente executa (render) → retorna JSX
2. React insere no DOM (commit)
3. useEffect com [] executa ← MONTAGEM
4. Se desmontar → cleanup (return) executa
```

## O cleanup da montagem

O `return` dentro do `useEffect` roda quando o componente desmonta — mesmo com `[]`:

```jsx
useEffect(() => {
  const id = setInterval(() => console.log("tick"), 1000);

  return () => clearInterval(id); // ← roda na desmontagem
}, []);
```

Sem o cleanup, o timer continua rodando depois do componente sair — vazamento de memória e `setState` em componente morto.

## Montagem vs re-montagem

```jsx
{mostrar && <Modal />} 
// Modal monta quando 'mostrar' vira true
// e DESMONTA quando vira false
// → o useEffect roda de novo a cada abertura
```

Se quer que um componente "renasça" do zero, a prop `key` força remontagem:

```jsx
<Detalhes key={produtoId} />
// mudou o produtoId → React desmonta e monta de novo
// → useEffect com [] roda de novo
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Fetch no corpo do componente | `useEffect` com `[]` |
| `setState` no effect sem proteção | Componente pode desmontar antes do fetch voltar — use flag ou AbortController |
| Listener sem cleanup | `return () => removeEventListener(...)` |
| Fazer setup no render | Render deve ser puro — setup vai no `useEffect` |

## Resumo

- `useEffect(() => {...}, [])` = roda uma vez, na montagem
- Casos clássicos: fetch inicial, localStorage, listeners, libs externas, foco
- Cleanup via `return` roda na desmontagem — sempre necessário para timers/listeners
- Re-montagem: renderização condicional e `key` mudam o ciclo
