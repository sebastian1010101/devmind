# FE04-26 — SASS: Instalação e Utilização Básica

## O que é SASS

**SASS** (Syntactically Awesome Style Sheets) é um pré-processador CSS — escreve-se numa sintaxe mais poderosa (`.scss`) e compila para CSS puro. Adiciona variáveis, aninhamento, mixins e lógica que o CSS sozinho não tem.

## Instalação no Vite

O Vite já entende SASS nativamente — só precisa instalar o compilador:

```bash
npm install -D sass
```

Nenhuma configuração extra. Arquivos `.scss` funcionam direto:

```jsx
import "./App.scss";        // em vez de .css
import styles from "./Card.module.scss"; // Modules também funcionam
```

## As features essenciais

### 1. Variáveis com `$`

```scss
$cor-primaria: #3498db;
$raio: 8px;
$espaco: 1rem;

.botao {
  background: $cor-primaria;
  border-radius: $raio;
  padding: $espaco;
}
```

### 2. Aninhamento (nesting)

```scss
.card {
  border: 1px solid #ddd;
  padding: 1rem;

  .titulo {
    font-size: 1.25rem;
  }

  .botao {
    margin-top: 1rem;

    &:hover {              // & = o seletor pai (.botao:hover)
      background: darken($cor-primaria, 10%);
    }
  }
}
```

```css
/* Compila para */
.card { border: 1px solid #ddd; padding: 1rem; }
.card .titulo { font-size: 1.25rem; }
.card .botao { margin-top: 1rem; }
.card .botao:hover { background: #217dbb; }
```

⚠️ **Cuidado com aninhamento excessivo** — 3 níveis no máximo, senão gera seletores específicos demais e frágeis.

### 3. Funções de cor

```scss
.botao {
  background: lighten(#3498db, 10%);    // mais claro
  border-color: darken(#3498db, 15%);   // mais escuro
  color: rgba(#fff, 0.9);
}
```

### 4. Partials — dividindo o CSS

```text
styles/
├── _variaveis.scss    ← começa com _ = não compila sozinho
├── _mixins.scss
├── _base.scss
└── main.scss          ← importa tudo
```

```scss
// _variaveis.scss
$cor-primaria: #3498db;

// main.scss
@use "variaveis" as v;
@use "base";

.botao {
  background: v.$cor-primaria;  // namespace evita colisões
}
```

### 5. Operadores e interpolação

```scss
$largura: 300px;

.lado-a-lado {
  width: $largura * 2;        // 600px — matemática nativa
}

@for $i from 1 through 3 {
  .m-#{$i} { margin: #{$i}rem; }  // .m-1, .m-2, .m-3
}
```

## SASS + CSS Modules

Funcionam juntos — `.module.scss`:

```scss
// Card.module.scss
.card {
  padding: 1rem;

  &:hover {
    transform: translateY(-4px);
  }
}
```

```jsx
import styles from "./Card.module.scss";
<div className={styles.card}>
```

## SASS vs CSS moderno

Com variáveis nativas e `clamp()`, muito do SASS virou redundante — mas ele ainda ganha em:

| SASS tem | CSS nativo tem |
| --- | --- |
| Mixins (reuso com parâmetros) | — |
| Aninhamento | Nativo desde 2023 |
| `@extend` (herança de estilos) | — |
| Lógica (`@if`, `@for`) | — |
| Variáveis compile-time | Variáveis runtime (`--var`) |

## Quando usar

- Projeto novo e pequeno → CSS puro + Modules já resolve
- Design system com temas e mixins → SASS brilha
- Código legado → você vai encontrar SASS em projetos reais

## Resumo

- `npm i -D sass` — Vite entende `.scss` sem configuração
- `$variaveis`, aninhamento com `&`, partials com `@use`
- Mixins e `@extend` no próximo tópico
- Não aninhe além de 3 níveis — seletores ficam frágeis
