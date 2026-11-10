# FE04-27 — Atividade: Estilizando um Componente com SASS

## Objetivo

Estilizar um componente React usando SASS — variáveis, aninhamento, partials e funções de cor.

## Setup

```bash
npm install -D sass
```

## Estrutura

```text
src/
├── styles/
│   ├── _variaveis.scss
│   └── _mixins.scss
├── components/
│   └── Botao/
│       ├── Botao.jsx
│       └── Botao.module.scss
└── App.jsx
```

## Partials compartilhadas

```scss
// src/styles/_variaveis.scss
$cor-primaria: #3498db;
$cor-perigo: #e74c3c;
$cor-sucesso: #22c55e;

$raio: 8px;
$espaco: 1rem;
$transicao: 0.2s ease;
```

## O componente estilizado

```scss
// src/components/Botao/Botao.module.scss
@use "../../styles/variaveis" as v;

.botao {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: v.$raio;
  font-weight: 600;
  cursor: pointer;
  transition: v.$transicao;

  // Variante primária (padrão)
  background: v.$cor-primaria;
  color: white;

  &:hover {
    background: darken(v.$cor-primaria, 10%);
    transform: translateY(-1px);
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

// Variantes
.perigo {
  background: v.$cor-perigo;

  &:hover {
    background: darken(v.$cor-perigo, 10%);
  }
}

.sucesso {
  background: v.$cor-sucesso;

  &:hover {
    background: darken(v.$cor-sucesso, 10%);
  }
}

.contorno {
  background: transparent;
  border: 2px solid v.$cor-primaria;
  color: v.$cor-primaria;

  &:hover {
    background: v.$cor-primaria;
    color: white;
  }
}
```

```jsx
// src/components/Botao/Botao.jsx
import styles from "./Botao.module.scss";

function Botao({ variante = "", children, ...rest }) {
  const classe = variante ? styles[variante] : "";

  return (
    <button
      className={`${styles.botao} ${classe}`}
      {...rest}
    >
      {children}
    </button>
  );
}

export default Botao;
```

## Uso

```jsx
import Botao from "./components/Botao/Botao";

function App() {
  return (
    <div style={{ display: "flex", gap: "1rem" }}>
      <Botao>Primário</Botao>
      <Botao variante="perigo">Excluir</Botao>
      <Botao variante="sucesso">Confirmar</Botao>
      <Botao variante="contorno">Contorno</Botao>
      <Botao disabled>Desabilitado</Botao>
    </div>
  );
}
```

## Desafios extras

### Desafio A — mixin de centralização

```scss
// _mixins.scss
@mixin centralizar {
  display: flex;
  align-items: center;
  justify-content: center;
}

// uso
.modal {
  @include centralizar;
}
```

### Desafio B — tamanhos via mapa

```scss
$tamanhos: (
  "pequeno": 0.4rem 0.8rem,
  "medio": 0.6rem 1.2rem,
  "grande": 0.8rem 1.6rem
);

@each $nome, $padding in $tamanhos {
  .#{$nome} {
    padding: $padding;
  }
}
```

## Critérios de verificação

- `npm i -D sass` instalado
- Variáveis em partial `_variaveis.scss` com `@use ... as v`
- Aninhamento com `&` para pseudo-classes
- Variantes como classes separadas no module
- Funções `darken()`/`lighten()` para hover states

## Erros comuns

| Erro | Correção |
| --- | --- |
| `@import "variaveis"` | `@use` é o moderno — `@import` está depreciado |
| `darken()` sem namespace | `v.$cor` se usou `as v` no `@use` |
| `.module.scss` sem `import styles` | Modules precisa do objeto `styles` |
| Aninhamento de 4+ níveis | Especificidade frágil — achate a estrutura |
