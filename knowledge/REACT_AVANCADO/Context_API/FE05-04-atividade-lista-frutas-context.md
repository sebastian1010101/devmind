# FE05-04 — Atividade: Refatorando uma Lista de Frutas com Context

## Objetivo

Pegar a atividade de lista de frutas (FE04-33) que usava `useState` local e refatorar para **Context API** — o estado das frutas fica disponível para qualquer componente.

## O antes — estado local

```jsx
function App() {
  const [frutas, setFrutas] = useState(["Maçã", "Banana"]);
  // só App e filhos diretos veem frutas
}
```

## O depois — Context

### 1. O contexto

```jsx
// contexts/FrutasContext.jsx
import { createContext, useState, useContext } from "react";

export const FrutasContext = createContext(null);

export function FrutasProvider({ children }) {
  const [frutas, setFrutas] = useState(["Maçã", "Banana", "Laranja"]);

  function adicionar(fruta) {
    setFrutas(f => [...f, fruta]);
  }

  function remover(nome) {
    setFrutas(f => f.filter(fr => fr !== nome));
  }

  return (
    <FrutasContext.Provider value={{ frutas, adicionar, remover }}>
      {children}
    </FrutasContext.Provider>
  );
}

export function useFrutas() {
  const ctx = useContext(FrutasContext);
  if (!ctx) throw new Error("useFrutas deve estar dentro de FrutasProvider");
  return ctx;
}
```

### 2. Envolver o app

```jsx
// App.jsx
import { FrutasProvider } from "./contexts/FrutasContext";

function App() {
  return (
    <FrutasProvider>
      <FormFruta />
      <ListaFrutas />
      <ContadorFrutas /> {/* em qualquer nível */}
    </FrutasProvider>
  );
}
```

### 3. Consumir nos componentes

```jsx
// components/ListaFrutas.jsx
import { useFrutas } from "../contexts/FrutasContext";

function ListaFrutas() {
  const { frutas, remover } = useFrutas();

  return (
    <ul>
      {frutas.map(f => (
        <li key={f}>
          {f}
          <button onClick={() => remover(f)}>×</button>
        </li>
      ))}
    </ul>
  );
}
```

```jsx
// components/FormFruta.jsx
function FormFruta() {
  const [nova, setNova] = useState("");
  const { adicionar } = useFrutas();

  function handleSubmit(e) {
    e.preventDefault();
    if (nova.trim()) {
      adicionar(nova.trim());
      setNova("");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={nova} onChange={e => setNova(e.target.value)} />
      <button>Adicionar</button>
    </form>
  );
}
```

```jsx
// components/ContadorFrutas.jsx — em outro ramo da árvore
function ContadorFrutas() {
  const { frutas } = useFrutas();
  return <p>{frutas.length} frutas</p>;
}
```

## O ganho — qualquer componente consome

```text
FrutasProvider
├── FormFruta     → adicionar() sem drilling
├── ListaFrutas   → frutas + remover() sem drilling
└── ContadorFrutas → frutas.length sem drilling
```

Sem Context, `frutas` teria que subir pro App e descer por props em todos.

## Desafios extras

### Desafio A — persistir no localStorage

```jsx
// dentro do FrutasProvider
useEffect(() => {
  localStorage.setItem("frutas", JSON.stringify(frutas));
}, [frutas]);
```

### Desafio B — frutas com quantidade

```jsx
// frutas vira array de objetos
{ id: 1, nome: "Maçã", qtd: 3 }
// adicionar aumenta qtd se já existe
```

### Desafio C — busca filtrada

```jsx
const [busca, setBusca] = useState("");
const filtradas = frutas.filter(f =>
  f.toLowerCase().includes(busca.toLowerCase())
);
```

## Critérios de verificação

- Contexto em `contexts/FrutasContext.jsx`
- `useFrutas` com validação de Provider
- `adicionar` e `remover` como actions do Provider
- Nenhum prop drilling de frutas
- `key` estável na lista

## Erros comuns

| Erro | Correção |
| --- | --- |
| Estado no App + Context | Um dono só — o Provider |
| `useContext` sem `useFrutas` | Hook customizado valida e limpa |
| Setter passado direto | Actions (`adicionar`, `remover`) encapsulam a lógica |
