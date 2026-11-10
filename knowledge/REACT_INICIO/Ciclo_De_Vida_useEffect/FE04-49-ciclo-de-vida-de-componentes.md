# FE04-49 — Ciclo de vida de componentes

## O que é o ciclo de vida

Todo componente React nasce, se atualiza e morre. Esse ciclo tem três fases:

```text
MONTAGEM                 ATUALIZAÇÃO                DESMONTAGEM
(mount)                  (update)                   (unmount)
   │                         │                          │
Componente criado      Estado ou props mudam       Componente removido
e inserido no DOM      e re-render acontece        da tela (condicional,
                            ↓                       rota, etc.)
Monta → renderiza →    Re-render → commit          Cleanup roda
commit no DOM          no DOM                      (limpar timers,
                            ↑                       listeners, fetch)
                  Pode repetir milhares
                  de vezes
```

## As três fases em detalhe

### 1. Montagem (Mount)

Acontece uma única vez — quando o componente aparece no DOM pela primeira vez.

```jsx
function Exemplo() {
  // 1. useState executa (valores iniciais)
  const [dados, setDados] = useState([]);

  // 2. Função executa → retorna JSX
  // 3. React insere no DOM
  // 4. useEffect com [] roda (DEPOIS do commit)

  useEffect(() => {
    console.log("Montou!"); // executa uma vez
    fetch("/api/dados").then(...)
  }, []);

  return <div>...</div>;
}
```

Momento ideal para: buscar dados, criar conexões, ler `localStorage`.

### 2. Atualização (Update)

Acontece toda vez que estado ou props mudam → novo render → React compara com o anterior (Virtual DOM) → aplica só o que mudou.

```jsx
useEffect(() => {
  console.log("dados mudou!");
}, [dados]); // roda quando 'dados' muda
```

Momento ideal para: sincronizar com mudanças, reagir a filtros, salvar estado no localStorage.

### 3. Desmontagem (Unmount)

Acontece quando o componente sai da tela — renderização condicional, mudança de rota, item removido da lista.

```jsx
useEffect(() => {
  const timer = setInterval(() => tick(), 1000);

  return () => {
    clearInterval(timer); // cleanup roda na desmontagem
  };
}, []);
```

Momento ideal para: limpar timers, remover listeners, cancelar requisições.

## Render vs Commit

O React separa duas fases internas:

```text
Render: a função executa, retorna JSX, React calcula o diff
       (pode ser pausada/repetida — deve ser PURA)

Commit: React aplica as mudanças no DOM real
       (e SÓ ENTÃO o useEffect roda)
```

Por isso `useEffect` é o lugar certo para efeitos colaterais — ele roda depois do DOM estar pronto.

## O legado: componentes de classe

Antes dos hooks, o ciclo de vida usava métodos de classe:

| Classe (legado) | Hook equivalente |
| --- | --- |
| `componentDidMount` | `useEffect(fn, [])` |
| `componentDidUpdate` | `useEffect(fn, [deps])` |
| `componentWillUnmount` | `return` dentro do useEffect |
| `shouldComponentUpdate` | `React.memo` |

Código moderno usa só hooks — mas entender a analogia ajuda a ler código legado.

## Por que o ciclo de vida importa

| Sem entender o ciclo | Com entendimento |
| --- | --- |
| Fetch no corpo do componente → loop infinito | Fetch no `useEffect` → uma vez |
| `setInterval` sem cleanup → vazamento de memória | `clearInterval` no return → limpo |
| Ler `localStorage` no render | Ler uma vez na montagem ou lazy init |

## Erros comuns

| Erro | Correção |
| --- | --- |
| Efeito colateral no corpo do componente | `useEffect` — o render deve ser puro |
| `useEffect` sem deps para "rodar sempre" | Pense se realmente precisa rodar a cada render |
| Esquecer cleanup de timer/listener | `return () => cleanup()` dentro do useEffect |
| `setState` depois de desmontar | Cleanup com flag/AbortController |

## Resumo

- Três fases: montagem (uma vez), atualização (toda mudança), desmontagem (ao sair)
- `useEffect` cobre as três: `[]` para montar, `[deps]` para atualizar, `return` para desmontar
- Render é puro — efeitos colaterais sempre no `useEffect`
