# FE04-64 — useEffect: Efeitos de desmontagem (parte 2)

## Além do óbvio — casos mais sutis

Na parte 1 vimos timers, listeners e fetch. Agora os casos mais avançados de cleanup.

## Cancelar animações e requestAnimationFrame

```jsx
function Animacao() {
  const frameRef = useRef(null);

  useEffect(() => {
    function animar() {
      // ...movimenta
      frameRef.current = requestAnimationFrame(animar);
    }
    frameRef.current = requestAnimationFrame(animar);

    return () => cancelAnimationFrame(frameRef.current);
  }, []);
}
```

## Intersection Observer / ResizeObserver

```jsx
const observerRef = useRef(null);

useEffect(() => {
  observerRef.current = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) setVisivel(true);
    });
  });

  observerRef.current.observe(elementoRef.current);

  return () => observerRef.current?.disconnect();
}, []);
```

## Assinaturas de estado global (zustand, redux, context)

```jsx
useEffect(() => {
  const unsubscribe = store.subscribe(estado => {
    setDados(estado.dados);
  });

  return () => unsubscribe(); // desinscreve na desmontagem
}, []);
```

## Subscriptions de bibliotecas

```jsx
useEffect(() => {
  const sub = servico.subscribe(dados => setDados(dados));
  return () => sub.unsubscribe();
}, []);
```

## Cleanup de múltiplos efeitos

Um componente pode ter vários `useEffect` — cada um com seu cleanup independente:

```jsx
// Efeito 1: timer
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}, []);

// Efeito 2: listener
useEffect(() => {
  window.addEventListener("resize", onResize);
  return () => window.removeEventListener("resize", onResize);
}, []);

// Efeito 3: fetch
useEffect(() => {
  const c = new AbortController();
  fetch(url, { signal: c.signal }).then(...);
  return () => c.abort();
}, [url]);
```

## O problema da requisição lenta

```jsx
// Cenário: usuário clica em outro item antes do fetch terminar
useEffect(() => {
  const c = new AbortController();

  async function carregar() {
    try {
      const res = await fetch(`/api/${id}`, { signal: c.signal });
      setDados(await res.json());
    } catch (e) {
      if (e.name === "AbortError") {
        console.log("Cancelado — componente desmontou ou id mudou");
      }
    }
  }

  carregar();
  return () => c.abort();
}, [id]); // aborta o anterior quando id muda
```

Sem `abort`: fetch do item A termina depois que o usuário já clicou no item B → mostra dados errados brevemente.

## Cleanup condicional — dependendo de props

```jsx
useEffect(() => {
  if (!conectado) return;

  const socket = new WebSocket(url);
  socket.onmessage = ...

  return () => socket.close();
}, [conectado, url]);
```

O cleanup só roda se o efeito executou o setup — `return` sem função significa "sem cleanup".

## O React 18 e o StrictMode

Em desenvolvimento, o React monta → **desmonta de propósito** → monta de novo. Seu cleanup é testado automaticamente:

```text
StrictMode simula:
1. Monta → useEffect roda (setup)
2. Simula desmontagem → cleanup roda
3. Monta de novo → useEffect roda de novo
```

Se a segunda montagem quebra, o cleanup está incompleto — ótimo aviso em dev, invisível em produção.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useRef` sem cancelar animação | `cancelAnimationFrame` no cleanup |
| Observer sem disconnect | `observer.disconnect()` no cleanup |
| Subscription sem unsubscribe | Salvar retorno e chamar no cleanup |
| Fetch sem abort em deps mutáveis | AbortController — cancela anterior |
| Cleanup quebrando a remontagem | StrictMode detecta — corrija o cleanup |

## O padrão universal

```jsx
useEffect(() => {
  // SETUP — cria recurso externo
  const recurso = criarRecurso();

  return () => {
    // CLEANUP — destrói/libera o recurso
    recurso.destroy();
  };
}, [deps]);
```

Tudo que **cria algo** fora do React precisa de **retorno que libera**.

## Resumo

- Cleanup cobre: timers, listeners, observers, websockets, subscriptions, rAF, fetch
- Com deps, cleanup roda antes de cada re-execução — evita acúmulo
- `AbortController` cancela fetch em desmontagem ou mudança de deps
- StrictMode em dev testa o cleanup — monta/desmonta/monta de propósito
