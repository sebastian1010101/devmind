# FE04-50 — useEffect: Introdução

## O que é o useEffect

`useEffect` é o hook que executa **efeitos colaterais** — tudo que sai do "renderizar UI": buscar dados, manipular DOM, timers, `localStorage`, assinaturas.

```jsx
import { useEffect } from "react";

useEffect(() => {
  // efeito colateral — roda DEPOIS do render
});
```

## As três formas

### Sem array de dependências — roda a cada render

```jsx
useEffect(() => {
  console.log("Rodou!");
}); // executa em TODO render — raramente é o que você quer
```

### Array vazio — roda só na montagem

```jsx
useEffect(() => {
  console.log("Montou!");
}, []); // uma única vez — requisições iniciais
```

### Array com dependências — roda quando algo muda

```jsx
useEffect(() => {
  console.log("busca mudou:", busca);
}, [busca]); // roda na montagem + toda vez que 'busca' muda
```

## Por que usar useEffect e não o corpo do componente

```jsx
// ❌ ERRADO — fetch dispara a cada render, gera loop infinito
function App() {
  const [dados, setDados] = useState([]);
  fetch("/api").then(r => r.json()).then(setDados);
  // setDados → re-render → fetch de novo → loop!

  return <div>...</div>;
}

// ✅ CERTO — fetch uma vez, na montagem
function App() {
  const [dados, setDados] = useState([]);

  useEffect(() => {
    fetch("/api").then(r => r.json()).then(setDados);
  }, []); // roda só quando o componente monta

  return <div>...</div>;
}
```

## A regra de ouro

> **Render puro, efeitos no useEffect.**

O corpo da função (o render) deve ser uma **função pura das props e do estado** — mesma entrada, mesmo JSX. Qualquer coisa que "suja" isso (rede, timers, DOM direto, storage) vai para o `useEffect`.

## Onde o useEffect roda na linha do tempo

```text
Componente executa (render)
        ↓
React calcula diff (Virtual DOM)
        ↓
React aplica mudanças no DOM real (commit)
        ↓
useEffect executa ← AQUI — depois do DOM estar pronto
        ↓
(usuario vê a tela antes do efeito terminar)
```

O efeito nunca bloqueia a pintura da tela — por isso fetch pesado vai aqui e não no render.

## Casos de uso clássicos

```jsx
// Buscar dados iniciais
useEffect(() => {
  fetch("/api/produtos").then(r => r.json()).then(setProdutos);
}, []);

// Sincronizar com uma prop/estado
useEffect(() => {
  document.title = `${notificacoes} notificações`;
}, [notificacoes]);

// Persistir estado
useEffect(() => {
  localStorage.setItem("tema", tema);
}, [tema]);

// Timer com cleanup
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}, []);
```

## StrictMode e o efeito duplo

Em desenvolvimento, o React `<StrictMode>` monta → desmonta → monta de propósito para detectar efeitos sem cleanup. Por isso em `dev` o console.log aparece duas vezes.

```text
StrictMode:
Monta → useEffect roda
Simula desmontagem → cleanup roda
Monta de novo → useEffect roda
```

Não é bug — é aviso: seu efeito precisa ter cleanup se toca recursos externos.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useEffect(async () => ...)` | O callback não pode ser async — declare a função dentro: `useEffect(() => { async function f(){...} f() }, [])` |
| Sem array de deps | Pense se realmente precisa rodar a cada render |
| Deps faltando | O ESLint `react-hooks` avisa — inclua tudo que o efeito usa |
| setState sem condição no efeito | Gera loop: efeito → setState → re-render → efeito |

## Resumo

- `useEffect` executa efeitos colaterais DEPOIS do render
- Três formas: sem deps (todo render), `[]` (montagem), `[deps]` (mudança)
- O render deve ser puro — rede, timers e DOM vão no `useEffect`
- Cleanup via `return () => ...` evita vazamentos
