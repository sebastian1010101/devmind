# FE04-28 — SASS: Mixins e Extend

## Mixins — CSS reutilizável com parâmetros

Um **mixin** é um bloco de CSS parametrizado — uma função que retorna estilos:

```scss
@mixin botao-base {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.botao {
  @include botao-base;
  background: blue;
}

.link-botao {
  @include botao-base;  // mesmas propriedades reutilizadas
  background: green;
}
```

### Mixins com parâmetros

```scss
@mixin flex($direcao: row, $gap: 0) {
  display: flex;
  flex-direction: $direcao;
  gap: $gap;
}

.lista {
  @include flex(column, 1rem);
}

.header {
  @include flex;  // usa os padrões
}
```

### Mixin com conteúdo dinâmico (@content)

```scss
@mixin mobile {
  @media (max-width: 768px) {
    @content;   // o bloco passado entra aqui
  }
}

.card {
  width: 300px;

  @include mobile {
    width: 100%;  // vira o @content dentro do media query
  }
}
```

### Mixins utilitários clássicos

```scss
@mixin centralizar-absoluto {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

@mixin texto-truncado {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@mixin card-sombra($nivel: 1) {
  @if $nivel == 1 {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  } @else if $nivel == 2 {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
}
```

## Extend — herança de estilos

`@extend` faz um seletor **herdar** as regras de outro — sem duplicar CSS:

```scss
.mensagem {
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid;
}

.mensagem-sucesso {
  @extend .mensagem;
  background: #d4edda;
  border-color: #22c55e;
}

.mensagem-erro {
  @extend .mensagem;
  background: #f8d7da;
  border-color: #e74c3c;
}
```

```css
/* Compila agrupando seletores — CSS enxuto */
.mensagem, .mensagem-sucesso, .mensagem-erro {
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid;
}
```

### Placeholders `%` — extend sem classe extra

```scss
// O % não vira classe no CSS — só serve de base para extend
%card-base {
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-produto {
  @extend %card-base;
  background: white;
}

.card-usuario {
  @extend %card-base;
  background: #f8f9fa;
}
```

## Mixin vs Extend — quando cada um

| | `@mixin` | `@extend` |
| --- | --- | --- |
| Aceita parâmetros | Sim | Não |
| CSS gerado | Duplica as regras em cada uso | Agrupa seletores (mais enxuto) |
| Flexibilidade | Alta (`@content`, `@if`) | Baixa |
| Use quando | Precisa de lógica/variação | Estilos idênticos entre classes |

Regra prática: **mixin é o padrão** — use `@extend` só quando a economia de CSS importa e os estilos são realmente idênticos.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `@extend` dentro de media query | Não funciona entre contextos diferentes |
| `@extend .classe-de-outro-arquivo` | Só funciona se o arquivo for `@use`'d |
| Mixin sem `@include` | `@mixin` define; `@include` usa |
| `@extend` com especificidade alta | Prefira mixin — extend complica a cascata |

## Resumo

- `@mixin nome { }` + `@include nome` — blocos reutilizáveis com parâmetros
- `@content` permite mixins que envolvem conteúdo (media queries)
- `@extend` compartilha estilos agrupando seletores
- `%placeholder` é a base para extend que não gera classe própria
- Em dúvida: mixin — mais flexível e previsível
