# FE04-62 — useRef: Entendendo o essencial

## O que é o useRef

`useRef` cria uma **referência mutável que não causa re-render** — uma "caixinha" que persiste entre renders sem disparar novo render quando muda.

```jsx
import { useRef } from "react";

function Exemplo() {
  const ref = useRef(valorInicial); // { current: valorInicial }

  ref.current = "novo valor"; // muda — mas NÃO re-renderiza
}
```

## Os dois usos

### 1. Acessar elementos do DOM

```jsx
function Formulario() {
  const inputRef = useRef(null);

  function focar() {
    inputRef.current.focus(); // DOM direto
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={focar}>Focar</button>
    </>
  );
}
```

A ref **"aguarda"** o elemento montar — `inputRef.current` é o `<input>` real do DOM.

### 2. Valor persistente sem re-render

```jsx
function Contador() {
  const contadorRef = useRef(0);
  const [exibicao, setExibicao] = useState(0);

  function incrementar() {
    contadorRef.current += 1;    // só na memória — não re-renderiza
    console.log(contadorRef.current);
  }

  function mostrar() {
    setExibicao(contadorRef.current); // agora sim aparece na tela
  }
}
```

## useRef vs useState

| `useState` | `useRef` |
| --- | --- |
| Mudança → re-render | Mudança → **sem** re-render |
| Valor na tela | Valor só na memória |
| `.current` invisível | `.current` é onde mora o valor |
| Ler e exibir | Ler e manipular DOM |

Regra: se o valor precisa aparecer na tela → `useState`. Se é só referência ou controle interno → `useRef`.

## Os casos de uso clássicos

### Foco, scroll, seleção de input

```jsx
useEffect(() => {
  inputRef.current?.focus();
  inputRef.current?.select(); // seleciona o texto
}, []);
```

### Guardar ID de timer

```jsx
const timerRef = useRef(null);

function iniciar() {
  timerRef.current = setInterval(tick, 1000);
}

function parar() {
  clearInterval(timerRef.current);
}
```

O timer precisa do ID pra ser cancelado — guardar em `useState` causaria re-render desnecessário.

### Valor anterior de estado/prop

```jsx
const anteriorRef = useRef(valor);

useEffect(() => {
  anteriorRef.current = valor; // guarda pra próxima vez
}, [valor]);

// anteriorRef.current tem o valor ANTES da mudança
```

### Contador de renders (debug)

```jsx
const renders = useRef(0);
renders.current += 1; // conta sem re-renderizar
console.log("Renderizou", renders.current, "vezes");
```

### Flag "já montou"

```jsx
const montou = useRef(false);

useEffect(() => {
  if (!montou.current) {
    montou.current = true;
    return;
  }
  // só roda nas atualizações
}, [dados]);
```

## Ref vs getElementById

```jsx
// ❌ Proibido no React — fora do controle
document.getElementById("meu-input").focus();

// ✅ Correto — ref aponta pro elemento do React
inputRef.current.focus();
```

React gerencia o DOM — `ref` é a ponte segura entre o JSX e o elemento real.

## forwardRef — passando ref pra componente filho

```jsx
import { forwardRef } from "react";

const InputCustom = forwardRef(function InputCustom(props, ref) {
  return <input ref={ref} {...props} />;
});

// pai
const inputRef = useRef(null);
<InputCustom ref={inputRef} />
inputRef.current.focus(); // funciona!
```

Sem `forwardRef`, o `ref` não chega ao DOM do filho.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `ref.current` no render (antes de montar) | `?.` e só acessar em efeitos/eventos |
| Mudar `.current` esperando re-render | `useRef` não dispara render — use `useState` se precisa mostrar |
| `ref` em componente sem `forwardRef` | Envolva o filho com `forwardRef` |
| Usar ref para substituir estado | Ref não re-renderiza — a tela não atualiza |

## Resumo

- `useRef` = valor mutável persistente, **sem** re-render
- Dois usos: acessar DOM (`.focus()`, `.scrollIntoView()`) e guardar valores internos (timers, contadores, valor anterior)
- `ref.current` só existe depois do mount — acesso em `useEffect` ou eventos
- `forwardRef` passa a ref para componentes filhos
