# FE05-49 — TypeScript no React: Instalação

## Criando projeto React + TS

```bash
# Vite — a forma moderna
npm create vite@latest meu-app -- --template react-ts

cd meu-app
npm install
```

O template `react-ts` já vem com tudo configurado.

## Projeto existente — adicionando TS

```bash
npm install --save-dev typescript @types/react @types/react-dom
```

Renomear arquivos:

```text
src/
├── App.jsx  →  App.tsx
├── main.jsx →  main.tsx
└── components/Botao.jsx → Botao.tsx
```

`.tsx` = TypeScript com JSX (o `x` habilita JSX).

## O tsconfig para React

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",          // transforma JSX sem import React
    "module": "ESNext",
    "strict": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "noEmit": true                // Vite compila, tsc só checa
  }
}
```

## Os @types — tipos das libs

```bash
npm install --save-dev @types/react @types/react-dom
```

`@types/*` traz as declarações de tipo de bibliotecas JS puras — o que permite ao TS entender `useState`, `JSX.Element`, etc.

## O que muda no código

```typescript
// sem TS — qualquer coisa
function Botao(props) {
  return <button>{props.texto}</button>;
}

// com TS — props tipadas
interface BotaoProps {
  texto: string;
  onClick?: () => void;
}

function Botao({ texto, onClick }: BotaoProps) {
  return <button onClick={onClick}>{texto}</button>;
}
```

## Tipos essenciais do React

```typescript
import type {
  ReactNode,        // qualquer coisa renderizável
  ReactElement,     // <div> — o JSX
  FC,               // FunctionComponent (desencorajado)
  CSSProperties,    // style={{}}
  MouseEvent,       // onClick
  ChangeEvent,      // onChange
  FormEvent,        // onSubmit
  KeyboardEvent
} from "react";
```

## O erro mais comum — `React.FC`

```tsx
// ⚠️ React.FC esconde children e generics
const Card: React.FC<Props> = ({ children }) => ...

// ✅ melhor — função normal com props tipadas
function Card({ children }: { children: ReactNode }) { ... }
```

`React.FC` é legado — funciona, mas mascarar props é pior.

## VS Code — IntelliSense no React

```text
Ctrl+Espaço    → autocomplete de props
Ctrl+Clique    → vai pra definição
Hover          → mostra os tipos
```

TS no React = IntelliSense completo de props, hooks e eventos.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `.jsx` com tipos | Renomeie para `.tsx` |
| `@types/react` faltando | `npm i -D @types/react @types/react-dom` |
| `React` importado sem uso | `"jsx": "react-jsx"` — não precisa importar |
| `any` nas props | Defina `interface Props` |

## Resumo

- `vite --template react-ts` — projeto pronto
- `.tsx` para componentes; `@types/react` para os tipos
- `ReactNode` para children; `interface` para props
- `strict: true` — o editor vira seu parceiro
