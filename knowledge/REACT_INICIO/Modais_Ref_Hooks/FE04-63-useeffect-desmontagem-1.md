# FE04-63 — useEffect: Efeitos de desmontagem (parte 1)

## O que é a desmontagem

Acontece quando o componente **sai da tela** — renderização condicional, mudança de rota, item removido da lista. O React destrói o DOM do componente e libera a memória.

```jsx
{mostrar && <Componente />} 
// mostrar vira false → Componente DESMONTA
// mostrar vira true → Componente MONTA de novo
```

## O cleanup — a função de retorno

O `useEffect` pode **retornar uma função** — ela roda antes da desmontagem (ou antes do próximo efeito, se houver deps):

```jsx
useEffect(() => {
  // Setup — roda na montagem/atualização
  const id = setInterval(tick, 1000);

  return () => {
    // Cleanup — roda na desmontagem / antes do próximo efeito
    clearInterval(id);
  };
}, []);
```

## Os casos de uso — o que precisa de cleanup

### 1. Timers (setInterval/setTimeout)

```jsx
useEffect(() => {
  const id = setInterval(() => {
    setSegundos(s => s + 1);
  }, 1000);

  return () => clearInterval(id);
}, []);
```

Sem o cleanup: o timer continua rodando depois do componente sumir — vazamento de memória e erro `setState em componente desmontado`.

### 2. Event listeners

```jsx
useEffect(() => {
  function aoScroll() {
    setPosicao(window.scrollY);
  }

  window.addEventListener("scroll", aoScroll);

  return () => window.removeEventListener("scroll", aoScroll);
}, []);
```

### 3. Assinaturas (websockets, observers)

```jsx
useEffect(() => {
  const socket = new WebSocket("wss://api.com");
  socket.onmessage = (e) => setMensagens(m => [...m, e.data]);

  return () => socket.close();
}, []);
```

### 4. Requisições — AbortController

```jsx
useEffect(() => {
  const controller = new AbortController();

  async function carregar() {
    try {
      const res = await fetch(url, { signal: controller.signal });
      const dados = await res.json();
      setDados(dados);
    } catch (e) {
      if (e.name !== "AbortError") setErro(e.message);
    }
  }

  carregar();

  return () => controller.abort(); // cancela se desmontar
}, [url]);
```

## A timeline completa

```text
Montagem:
  render → commit → useEffect (setup)

Atualização:
  deps mudam → cleanup do efeito anterior → setup novo

Desmontagem:
  React remove do DOM → cleanup de todos os efeitos
```

## O erro clássico — setState após desmontar

```jsx
// ❌ Aviso no console: "Can't perform a React state update 
//    on an unmounted component"
useEffect(() => {
  fetch("/api").then(r => r.json()).then(setDados); 
  // se desmontar antes do fetch voltar → erro
}, []);
```

Soluções:

```jsx
// Opção A — AbortController (melhor)
useEffect(() => {
  const c = new AbortController();
  fetch(url, { signal: c.signal }).then(...);
  return () => c.abort();
}, []);

// Opção B — flag de montagem
useEffect(() => {
  let ativo = true;
  fetch(url).then(r => r.json()).then(d => {
    if (ativo) setDados(d);
  });
  return () => { ativo = false; };
}, []);
```

## Cleanup na atualização — não só na desmontagem

Com deps, o cleanup roda **antes de cada novo efeito** também:

```jsx
useEffect(() => {
  const id = setInterval(tick, intervalo);
  return () => clearInterval(id); // limpa o timer ANTIGO
}, [intervalo]); // novo timer com o novo intervalo
```

Mudou `intervalo` → React limpa o timer anterior → cria um novo. Sem cleanup, acumularia timers.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `setInterval` sem cleanup | `return () => clearInterval(id)` |
| `addEventListener` sem remove | `return () => removeEventListener(...)` |
| Fetch sem cancelamento | `AbortController` + `return () => abort()` |
| `setState` após desmontar | Flag `ativo` ou AbortController |
| Cleanup só na desmontagem, esquecendo atualização | O cleanup roda também antes de re-executar com deps |

## Resumo

- `return () => ...` no `useEffect` = função de cleanup
- Roda na desmontagem E antes de re-executar o efeito
- Obrigatório para: timers, listeners, websockets, fetch com abort
- Sem cleanup → vazamento de memória, setState em componente morto
