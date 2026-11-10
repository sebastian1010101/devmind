# FE04-42 — Estado: Performance

## Quando o estado vira problema de performance

Cada mudança de estado dispara re-render — e re-render custa. Em apps grandes, renders desnecessários acumulam: listas que re-renderizam 1000 itens porque um checkbox mudou, componentes filhos re-renderizando sem precisar.

## O que causa re-render

```text
1. Estado local muda (setState)
2. Props recebidas mudam (nova referência)
3. Pai re-renderiza → filho re-renderiza junto (mesmo sem prop mudar)
4. Contexto consumido muda
```

O item 3 é o surpreendente: **pai re-renderiza, filho re-renderiza** — mesmo que as props do filho não mudaram.

## Diagnóstico: quem está re-renderizando?

### React DevTools Profiler

```text
DevTools → Profiler → Record → interaja → pare
```

Mostra cada componente que renderizou, quanto tempo levou e **por quê** — essencial para achar renders desnecessários.

### Log de render (rápido para depuração)

```jsx
function Componente({ data }) {
  console.log("Componente renderizou"); // quantas vezes aparece?
  return <div>{data}</div>;
}
```

## As otimizações

### 1. React.memo — memoriza o componente

Impede re-render do filho quando as props não mudaram:

```jsx
import { memo } from "react";

const ItemCaro = memo(function ItemCaro({ produto }) {
  // Só re-renderiza se 'produto' mudar de referência
  return <div>{produto.nome}</div>;
});
```

```jsx
// Pai re-renderiza, mas ItemCaro só re-renderiza se a prop mudou
<Lista>
  {itens.map(i => <ItemCaro key={i.id} produto={i} />)}
</Lista>
```

### 2. useMemo — memoriza cálculo custoso

```jsx
// ❌ Recalcula a cada render — mesmo sem itens mudar
const total = itens.reduce((acc, i) => acc + i.preco, 0);

// ✅ Só recalcula quando 'itens' muda
const total = useMemo(
  () => itens.reduce((acc, i) => acc + i.preco, 0),
  [itens]
);
```

### 3. useCallback — memoriza função

Funções recriadas a cada render quebram o `memo` dos filhos:

```jsx
// ❌ Nova função a cada render — memo do filho falha
<ItemCaro onClick={() => remover(item.id)} />

// ✅ Função estável — memo funciona
const remover = useCallback((id) => {
  setItens(prev => prev.filter(i => i.id !== id));
}, []);

<ItemCaro onClick={remover} />
```

### 4. Estado localizado — desça o estado

```jsx
// ❌ Estado no topo re-renderiza tudo
function App() {
  const [input, setInput] = useState(""); // cada tecla re-renderiza App inteira
  return (
    <>
      <ListaGigante />  {/* re-renderiza desnecessariamente */}
      <Form input={input} setInput={setInput} />
    </>
  );
}

// ✅ Estado perto de quem usa
function Form() {
  const [input, setInput] = useState(""); // só Form re-renderiza
}
```

## A regra de ouro

**Não otimize antes de medir.** `memo`, `useMemo` e `useCallback` têm custo (comparação de props + memória). Use-os quando:

- O Profiler mostra renders desnecessários de componentes pesados
- Listas grandes re-renderizam por mudança pequena
- Funções quebram `memo` dos filhos

Para 90% dos componentes, a re-renderização é instantânea — otimize só onde dói.

## Erros comuns

| Erro | Por que falha |
| --- | --- |
| `memo` sem `useCallback` nas props | Função nova a cada render quebra o memo |
| `useMemo` em tudo | Overhead maior que o ganho — otimize só o caro |
| Estado global para dado local | Re-renderiza a árvore inteira |
| `key={index}` em lista grande | Reordenação quebra memo e estado interno |

## Resumo

- Pai renderiza → filho renderiza junto (mesmo sem prop nova)
- `React.memo` para componentes, `useMemo` para cálculos, `useCallback` para funções
- Estado localizado > estado no topo
- Meça com o Profiler — otimize onde dói, não preventivamente
