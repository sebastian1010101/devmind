# FE05-29 — Atividade: Criando um Dark Mode com Jotai

## Objetivo

Tema claro/escuro com Jotai — átomo de tema, persistência automática e componentes que reagem sem props.

## O átomo de tema

```jsx
// store/temaAtom.js
import { atomWithStorage } from "jotai/utils";

// persiste automaticamente — reload mantém o tema
export const temaAtom = atomWithStorage("tema", "claro");
```

## O componente de toggle

```jsx
// components/ToggleTema.jsx
import { useAtom } from "jotai";
import { temaAtom } from "../store/temaAtom";

function ToggleTema() {
  const [tema, setTema] = useAtom(temaAtom);

  return (
    <button
      onClick={() => setTema(t => t === "claro" ? "escuro" : "claro")}
      className="toggle-tema"
    >
      {tema === "claro" ? "🌙" : "☀️"}
    </button>
  );
}
```

## O provider de tema no CSS

```jsx
// components/TemaWrapper.jsx
import { useAtomValue } from "jotai";
import { useEffect } from "react";
import { temaAtom } from "../store/temaAtom";

function TemaWrapper({ children }) {
  const tema = useAtomValue(temaAtom);

  useEffect(() => {
    document.documentElement.dataset.tema = tema;
  }, [tema]);

  return <>{children}</>;
}
```

```css
/* styles/global.css */
:root[data-tema="claro"] {
  --fundo: #ffffff;
  --texto: #1a1a1a;
  --card: #f5f5f5;
  --borda: #e0e0e0;
}

:root[data-tema="escuro"] {
  --fundo: #1a1a1a;
  --texto: #eeeeee;
  --card: #2d2d2d;
  --borda: #404040;
}

body {
  background: var(--fundo);
  color: var(--texto);
  transition: background 0.3s, color 0.3s;
}
```

## Componentes consumindo o tema

```jsx
function Card({ children }) {
  const tema = useAtomValue(temaAtom); // lê direto — sem props

  return (
    <div className={`card ${tema}`}>
      {children}
    </div>
  );
}
```

## Átomo derivado — informações do tema

```jsx
// átomo que só lê — deriva do principal
export const temaInfoAtom = atom((get) => {
  const tema = get(temaAtom);
  return {
    atual: tema,
    eEscuro: tema === "escuro",
    icone: tema === "claro" ? "🌙" : "☀️",
    proximo: tema === "claro" ? "escuro" : "claro"
  };
});

// uso
const { eEscuro, icone, proximo } = useAtomValue(temaInfoAtom);
```

## Toggle avançado — com átomo de escrita

```jsx
export const alternarTemaAtom = atom(
  null,
  (get, set) => {
    const atual = get(temaAtom);
    set(temaAtom, atual === "claro" ? "escuro" : "claro");
  }
);

// componente — só dispara
const alternar = useSetAtom(alternarTemaAtom);
<button onClick={alternar}>Alternar</button>
```

## A estrutura

```jsx
function App() {
  return (
    <TemaWrapper>
      <Header>
        <ToggleTema />
      </Header>
      <main>
        <Card>Conteúdo que muda com o tema</Card>
      </main>
    </TemaWrapper>
  );
}
```

```text
TemaWrapper
  ├── lê temaAtom → aplica no <html>
  ├── ToggleTema → escreve temaAtom
  └── Card → lê temaAtom → classe condicional
```

## Desafios extras

### Desafio A — tema do sistema

```jsx
const temaSistemaAtom = atom(
  window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "escuro"
    : "claro"
);

const temaAtom = atomWithStorage(
  "tema",
  null // null = segue o sistema
);
```

### Desafio B — múltiplas preferências

```jsx
export const preferenciasAtom = atomWithStorage("prefs", {
  tema: "claro",
  fonte: "media",
  animacoes: true
});

// atom derivado para cada preferência
export const temaAtom = atom(
  (get) => get(preferenciasAtom).tema,
  (get, set, novo) => {
    set(preferenciasAtom, {
      ...get(preferenciasAtom),
      tema: novo
    });
  }
);
```

### Desafio C — transição suave

```css
* {
  transition: background-color 0.3s, color 0.3s;
}
```

## Critérios de verificação

- `atomWithStorage` — reload mantém o tema
- `useAtomValue` para leitura; `useAtom` ou `useSetAtom` para escrita
- CSS com variáveis em `:root[data-tema]`
- Sem props de tema — componentes consomem direto
- `data-tema` no `document.documentElement` via `useEffect`

## Erros comuns

| Erro | Correção |
| --- | --- |
| `atom` dentro de componente | Declare fora — é global |
| `useAtom` quando só lê | `useAtomValue` — não se inscreve pra escrita |
| Tema sem persistência | `atomWithStorage` em vez de `atom` |
| CSS hardcoded por classe | Variáveis em `:root[data-tema]` |
