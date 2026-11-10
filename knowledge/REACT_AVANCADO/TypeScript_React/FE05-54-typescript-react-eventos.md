# FE05-54 — TypeScript no React: Eventos

## Os tipos de evento do React

```tsx
import type {
  MouseEvent,     // onClick, onMouseEnter...
  ChangeEvent,    // onChange de input/select
  FormEvent,      // onSubmit
  KeyboardEvent,  // onKeyDown/onKeyUp
  FocusEvent,     // onFocus/onBlur
  DragEvent,      // onDragStart...
  WheelEvent,     // onWheel
  SyntheticEvent  // a base de todos
} from "react";
```

## onClick — MouseEvent

```tsx
function Botao() {
  function handleClick(e: MouseEvent<HTMLButtonElement>) {
    e.preventDefault();
    console.log(e.currentTarget.textContent);
  }

  return <button onClick={handleClick}>Clique</button>;
}
```

Generic `<HTMLButtonElement>` — o tipo do elemento que disparou.

## onChange — ChangeEvent

```tsx
function Input() {
  const [valor, setValor] = useState("");

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    setValor(e.target.value); // e.target é HTMLInputElement
  }

  // select é HTMLSelectElement
  function handleSelect(e: ChangeEvent<HTMLSelectElement>) {
    // ...
  }

  // textarea é HTMLTextAreaElement
  function handleArea(e: ChangeEvent<HTMLTextAreaElement>) {
    // ...
  }
}
```

## onSubmit — FormEvent

```tsx
function Formulario() {
  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const dados = new FormData(e.currentTarget);
    const nome = dados.get("nome") as string;
  }

  return <form onSubmit={handleSubmit}>...</form>;
}
```

## onKeyDown — KeyboardEvent

```tsx
function Busca() {
  function handleKey(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") buscar();
    if (e.key === "Escape") limpar();
    if (e.ctrlKey && e.key === "k") abrirBusca();
  }

  return <input onKeyDown={handleKey} />;
}
```

## Tipando o elemento — o generic importa

```tsx
// errado — target é Element genérico
(e: ChangeEvent) => e.target.value // ❌ .value não existe em Element

// certo — target é HTMLInputElement
(e: ChangeEvent<HTMLInputElement>) => e.target.value // ✅
```

## Tabela de eventos comuns

| Evento | Tipo | Elemento |
| --- | --- | --- |
| `onClick` | `MouseEvent` | `HTMLButtonElement` |
| `onChange` (input) | `ChangeEvent` | `HTMLInputElement` |
| `onChange` (select) | `ChangeEvent` | `HTMLSelectElement` |
| `onSubmit` | `FormEvent` | `HTMLFormElement` |
| `onKeyDown` | `KeyboardEvent` | `HTMLInputElement` |
| `onFocus` | `FocusEvent` | `HTMLInputElement` |
| `onMouseEnter` | `MouseEvent` | `HTMLDivElement` |

## Callback props tipados

```tsx
interface FormProps {
  onSubmit: (dados: FormularioData) => void;
  onCancelar: () => void;
}

function Form({ onSubmit, onCancelar }: FormProps) {
  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    onSubmit({ nome, email });
  }
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `e: any` | `ChangeEvent<HTMLInputElement>` etc. |
| `e.target.value` sem generic | `ChangeEvent<HTMLInputElement>` — target tipado |
| `FormEvent` vs `FormEvent<HTMLFormElement>` | Generic no formulário |
| Callback com `Function` | `() => void` — assinatura específica |

## Resumo

- Cada evento tem um tipo React: `MouseEvent`, `ChangeEvent`, `FormEvent`, `KeyboardEvent`
- O generic `<HTMLElement>` tipa `e.target`/`e.currentTarget`
- Callbacks em props: `() => void` ou com parâmetros tipados
- `FormEvent<HTMLFormElement>` para `onSubmit`
