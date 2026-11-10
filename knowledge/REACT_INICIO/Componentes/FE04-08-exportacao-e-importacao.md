# FE04-08 — Componentes: Exportação e Importação

## Por que modularizar

Um componente por arquivo mantém o código navegável — mas para usar um componente de outro arquivo, você precisa **exportar** ele de lá e **importar** onde será usado. É o mesmo sistema de módulos ES6, agora aplicado a componentes.

## Export default — um por arquivo

O padrão mais comum em React: cada arquivo exporta um componente principal:

```jsx
// src/components/Button.jsx
function Button() {
  return <button>Clique</button>;
}

export default Button;
```

```jsx
// src/components/Header.jsx
import Button from "./Button"; // sem chaves, nome livre

function Header() {
  return (
    <header>
      <h1>Meu App</h1>
      <Button />
    </header>
  );
}
```

## Named exports — vários por arquivo

Quando um arquivo agrupa utilidades ou componentes relacionados:

```jsx
// src/components/ui.jsx
export function Button() {
  return <button>Botão</button>;
}

export function Input() {
  return <input />;
}

export function Label({ children }) {
  return <label>{children}</label>;
}
```

```jsx
// importa com chaves, nomes exatos
import { Button, Input, Label } from "./ui";
```

## Export default vs Named

| | `export default` | `export` (named) |
| --- | --- | --- |
| Quantidade por arquivo | 1 | Quantos quiser |
| Import | `import Nome from "..."` — nome livre | `import { nome } from "..."` — nome fixo |
| Renomear | No import direto | `import { nome as outro }` |
| Convenção React | Componente principal do arquivo | Utilidades, helpers, subcomponentes |

```jsx
// Um arquivo pode ter os dois
export default function Header() { }
export const LOGO_SIZE = 40;
export const NavItem = () => { };
```

## Estrutura de pastas padrão

```text
src/
├── App.jsx
├── main.jsx
└── components/
    ├── Header/
    │   ├── Header.jsx        ← componente
    │   ├── Header.module.css ← estilos (CSS Modules)
    │   └── index.js          ← re-export para import limpo
    ├── Button/
    │   ├── Button.jsx
    │   └── index.js
    └── Card/
        ├── Card.jsx
        └── index.js
```

### O truque do index.js

```javascript
// src/components/Header/index.js
export { default } from "./Header";
```

Permite importar sem o caminho interno:

```jsx
// Com index.js — import limpo
import Header from "./components/Header";

// Sem index.js — caminho completo necessário
import Header from "./components/Header/Header";
```

## Importações relativas

```jsx
import Button from "./Button";                    // mesma pasta
import Card from "../components/Card";            // sobe um nível
import { formatar } from "../../utils/format";    // sobe dois níveis
```

## Renomeando no import

```jsx
// Named import renomeado
import { Button as BotaoPrimario } from "./ui";

// Útil para conflitos de nome
import { Button } from "./ui";
import { Button as BootstrapButton } from "./bootstrap";
```

## Import dinâmico

Para código que só carrega quando necessário (code splitting):

```jsx
const Modal = lazy(() => import("./components/Modal"));

// ou import() direto
const modulo = await import("./utils");
```

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| `import { Header }` quando é `export default` | `undefined` — default não usa chaves |
| `export` sem `default` + `import X` | `undefined` — named precisa de chaves |
| Caminho errado `./Button` vs `./button` | Case-sensitive — confira maiúsculas |
| Sem `./` no caminho | `import "Button"` busca em node_modules — precisa de `./` |
| `index.js` com `export * from` | Pode gerar circular imports — prefira `export { default }` |

## Resumo

- `export default` para o componente principal do arquivo
- Named exports para utilidades e componentes auxiliares
- `index.js` em cada pasta de componente para imports limpos
- Import com `{}` para named, sem `{}` para default
