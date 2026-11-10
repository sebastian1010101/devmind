# FE04-43 — Styled Components: Introdução

## O que é

**Styled Components** é a biblioteca CSS-in-JS mais popular do ecossistema React — você escreve CSS dentro de template literals do JavaScript, e cada estilo gera um componente React com escopo automático.

```bash
npm install styled-components
```

## O básico

```jsx
import styled from "styled-components";

// Cria um <button> estilizado — escopo automático
const Botao = styled.button`
  background: #3498db;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;

  &:hover {
    background: #2980b9;
  }
`;

// Usa como componente normal
function App() {
  return <Botao>Clique</Botao>;
}
```

A classe gerada é única (`sc-hash`) — colisão impossível, igual CSS Modules.

## Anatomia

```jsx
const Elemento = styled.tagHTML`
  /* CSS puro — com acesso a props */
`;
```

- `styled.button`, `styled.div`, `styled.a` — qualquer tag HTML
- Estilos de componente: `styled(OutroComponente)`
- Template literal = o CSS é uma string com acesso ao JS

## Vantagens vs CSS tradicional

| Aspecto | Styled Components | CSS Modules |
| --- | --- | --- |
| Escopo | Automático (hash) | Automático (hash) |
| Props → estilo | Direto (`${props =>}`) | Precisa de classes condicionais |
| CSS morto | Não existe — componente existe ou não | Pode sobrar arquivo órfão |
| Theming | `ThemeProvider` nativo | Variáveis CSS manuais |
| Sintaxe | CSS dentro de JS | CSS puro |

## Props dinâmicas

O diferencial: o estilo **reage a props** sem classes condicionais:

```jsx
const Botao = styled.button`
  background: ${props => props.$primario ? "#3498db" : "#ccc"};
  padding: ${props => props.$grande ? "1rem 2rem" : "0.6rem 1.2rem"};
`;

<Botao $primario $grande>Salvar</Botao>
```

O prefixo `$` (transient props) impede que a prop vá para o DOM — sem o `$`, o React avisa sobre atributos desconhecidos.

## Pseudo-classes e media queries

```jsx
const Card = styled.div`
  padding: 1rem;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-4px);
  }

  &:last-child {
    margin-bottom: 0;
  }

  @media (max-width: 768px) {
    padding: 0.5rem;
  }
`;
```

CSS completo dentro do template — `&`, `@media`, pseudo-elementos, tudo funciona.

## Estendendo componentes

```jsx
const Botao = styled.button`
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
`;

const BotaoPerigo = styled(Botao)`
  background: #e74c3c;
`;

const BotaoSucesso = styled(Botao)`
  background: #22c55e;
`;
```

## Quando usar vs CSS Modules

| Situação | Escolha |
| --- | --- |
| Estilos que dependem de props | Styled Components |
| Design system com temas | Styled Components + ThemeProvider |
| CSS estático simples | CSS Modules é suficiente |
| Time que prefere CSS puro | CSS Modules |
| Performance crítica | CSS Modules (sem runtime JS) |

## Erros comuns

| Erro | Correção |
| --- | --- |
| Prop sem `$` indo pro DOM | Use `$prop` — transient props |
| Styled dentro do componente | Define fora — dentro recria a cada render |
| `styled.div` para componente | `styled(Componente)` para estilizar componentes |
| CSS gigante num styled | Divida em componentes menores |

## Resumo

- `styled.tag` + template literal = componente com escopo automático
- Props dinâmicas com `${props =>}` — o superpoder do CSS-in-JS
- `$` prefix para transient props (não vão ao DOM)
- Ideal quando o estilo precisa reagir a props e temas
