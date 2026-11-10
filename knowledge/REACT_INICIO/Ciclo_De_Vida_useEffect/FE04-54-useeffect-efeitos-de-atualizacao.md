# FE04-54 — useEffect: Efeitos de atualização

## O que é um efeito de atualização

Um efeito que roda quando **dependências mudam** — não só na montagem, mas toda vez que as variáveis listadas são atualizadas.

```jsx
useEffect(() => {
  console.log("busca mudou:", busca);
}, [busca]); // montagem + toda mudança de 'busca'
```

## Como funciona o array de dependências

React compara cada item do array com o valor da render anterior — se qualquer um mudou, o efeito roda de novo:

```jsx
useEffect(() => {
  console.log("Roda na montagem e quando a ou b mudam");
}, [a, b]); // múltiplas dependências
```

## Os casos de uso

### 1. Sincronizar estado com localStorage

```jsx
const [favoritos, setFavoritos] = useState(() => 
  JSON.parse(localStorage.getItem("favoritos") || "[]")
);

useEffect(() => {
  localStorage.setItem("favoritos", JSON.stringify(favoritos));
}, [favoritos]); // salva toda vez que a lista muda
```

### 2. Reagir a props de um pai

```jsx
function DetalhesProduto({ produtoId }) {
  const [produto, setProduto] = useState(null);

  useEffect(() => {
    async function carregar() {
      const res = await fetch(`/api/produtos/${produtoId}`);
      setProduto(await res.json());
    }
    carregar();
  }, [produtoId]); // recarrega quando o id muda
```

### 3. Busca com debounce (pesquisa ao digitar)

```jsx
const [busca, setBusca] = useState("");

useEffect(() => {
  if (!busca.trim()) return;

  const timer = setTimeout(() => {
    fetch(`/api/busca?q=${busca}`).then(r => r.json()).then(setResultados);
  }, 500); // espera 500ms de pausa de digitação

  return () => clearTimeout(timer); // cancela se digitar de novo
}, [busca]);
```

### 4. Atualizar título da página

```jsx
useEffect(() => {
  document.title = `${notificacoes} novas mensagens`;
}, [notificacoes]); // título muda quando o contador muda
```

### 5. Rolar para o fim quando novas mensagens chegam

```jsx
useEffect(() => {
  chatRef.current?.scrollTo(0, chatRef.current.scrollHeight);
}, [mensagens]); // desce o scroll ao chegar mensagem nova
```

## Montagem + atualização vs só atualização

`useEffect` com deps **sempre roda na montagem também**. Se precisa pular a primeira vez:

```jsx
const montou = useRef(false);

useEffect(() => {
  if (!montou.current) {
    montou.current = true;
    return; // pula a montagem
  }

  console.log("Só atualizações!");
}, [dados]);
```

## O loop infinito — o perigo nº 1

```jsx
// ❌ LOOP INFINITO
useEffect(() => {
  setContador(c => c + 1); // muda estado → re-render → efeito de novo
}); // sem deps, ou dependendo do próprio contador

// ❌ também loop
useEffect(() => {
  setDados([...dados, novoItem]);
}, [dados]); // muda o que observa

// ✅ condição de saída
useEffect(() => {
  if (dados.length === 0) {
    setDados(dadosIniciais);
  }
}, [dados]); // só roda se vazio — para no próximo ciclo
```

Regra: se o efeito modifica uma dependência, garanta que a mudança **converge** — senão é loop.

## Dependências — o que colocar

O array deve listar **tudo que o efeito usa de fora**:

```jsx
useEffect(() => {
  fetch(url).then(...)
    .then(d => setDados(d))
    .catch(e => setErro(e));
}, [url]); // 'url' usada → deve estar nas deps
```

```jsx
// ❌ ESLint reclama — 'formato' usado mas não listado
useEffect(() => {
  salvar(dados, formato);
}, [dados]);

// ✅ correto
useEffect(() => {
  salvar(dados, formato);
}, [dados, formato]);
```

### Objetos e arrays como dependências

```jsx
// ⚠️ Cuidado — objeto recriado a cada render
const config = { tema: "escuro" };
useEffect(() => { ... }, [config]); // roda a cada render (nova referência)

// ✅ primitivos são seguros
const tema = "escuro";
useEffect(() => { ... }, [tema]);

// ✅ ou useMemo para estabilizar
const config = useMemo(() => ({ tema: "escuro" }), []);
```

## Montagem vs atualização — o padrão completo

```jsx
useEffect(() => {
  // Montagem: roda
  // Atualização: roda quando 'url' muda
  // Desmontagem: cleanup roda
  
  const controller = new AbortController();
  fetch(url, { signal: controller.signal }).then(...);

  return () => controller.abort();
}, [url]);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Efeito modifica a dependência que observa | Condicione a mudança ou use outro estado |
| Objeto/array nas deps recriado a cada render | `useMemo`/`useCallback` ou dependa de primitivos |
| Falta de dependência → valor velho | Liste tudo que o efeito usa |
| Loop por setState sem condição | O efeito deve convergir — não mudar o que observa |

## Resumo

- `[deps]` roda na montagem + cada mudança das dependências
- Casos: sync com storage, reagir a props, debounce, efeitos no DOM
- Loop infinito: efeito modifica o que observa sem condição de parada
- Dependências devem ser completas e estáveis (primitivos ou memoizados)
