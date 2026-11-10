# FE04-45 — Styled Components: Props em Componentes de Estilo

## O diferencial real

Props transformam styled components em sistemas de variantes — um componente, várias aparências, sem multiplicar classes CSS.

## Props básicas

```jsx
const Botao = styled.button`
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  border: none;
  color: white;
  background: ${props => props.$cor || "#3498db"};
`;

<Botao>Primário</Botao>                    {/* azul padrão */}
<Botao $cor="#e74c3c">Excluir</Botao>       {/* vermelho */}
<Botao $cor="#22c55e">Confirmar</Botao>     {/* verde */}
```

## Transient props — o prefixo `$`

Props com `$` são consumidas pelo styled e **não vão para o DOM** — sem o `$`, o React avisa sobre atributo desconhecido:

```jsx
// ❌ 'primario' vira atributo HTML desconhecido — warning
const Botao = styled.button`
  background: ${props => props.primario ? "blue" : "gray"};
`;
<Botao primario /> // <button primario="true"> — inválido

// ✅ '$primario' é consumido pelo styled, não renderiza
const Botao = styled.button`
  background: ${props => props.$primario ? "#3498db" : "#ccc"};
`;
<Botao $primario /> // <button> limpo
```

## Variantes com props booleanas

```jsx
const Botao = styled.button`
  padding: ${p => p.$grande ? "1rem 2rem" : "0.6rem 1.2rem"};
  font-size: ${p => p.$grande ? "1.1rem" : "0.9rem"};
  border-radius: 6px;
  border: none;
  color: white;

  background: ${p => {
    if (p.$perigo) return "#e74c3c";
    if (p.$sucesso) return "#22c55e";
    return "#3498db";
  }};

  ${p => p.$contorno && `
    background: transparent;
    border: 2px solid #3498db;
    color: #3498db;
  `}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;
```

```jsx
<Botao>Normal</Botao>
<Botao $grande>Grande</Botao>
<Botao $perigo>Excluir</Botao>
<Botao $sucesso $grande>Confirmar</Botao>
<Botao $contorno>Contorno</Botao>
```

## Props com valores dinâmicos

```jsx
const Barra = styled.div`
  width: ${p => p.$progresso}%;
  height: 8px;
  background: ${p =>
    p.$progresso < 30 ? "#e74c3c" :
    p.$progresso < 70 ? "#f39c12" : "#22c55e"};
  transition: width 0.3s;
`;

<Barra $progresso={75} />
```

## Combinando com o tema

```jsx
const Card = styled.article`
  background: ${p => p.theme.superficie};
  border: 1px solid ${p => p.theme.borda};
  padding: ${p => p.$compacto ? "0.5rem" : "1.5rem"};
`;
```

Props locais (`$compacto`) + tema global (`theme`) — as duas fontes de dinamismo convivem.

## attrs — atributos fixos

```jsx
const Input = styled.input.attrs({
  type: "text",
  autoComplete: "off"
})`
  padding: 0.5rem;
  border: 1px solid var(--cor-borda);
`;
```

```jsx
// attrs com função — atributos dinâmicos
const Link = styled.a.attrs(p => ({
  target: p.$externo ? "_blank" : undefined
}))`
  color: ${p => p.theme.primaria};
`;
```

## A convenção de nomes

| Prop | Uso |
| --- | --- |
| `$primario`, `$perigo` | Variantes booleanas |
| `$grande`, `$compacto` | Tamanhos |
| `$ativo`, `$selecionado` | Estados |
| `$cor`, `$largura` | Valores arbitrários |

Prefixo `$` + camelCase descritivo — o padrão da comunidade.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Prop vai pro DOM (warning) | Prefixe com `$` |
| `$prop` no HTML | `$` é transient — não aparece no DOM final |
| Lógica gigante no template | Extraia para função helper se crescer |
| Props dinâmicas com `style` inline | Styled props são mais limpas e testáveis |

## Resumo

- `$prop` = transient prop — alimenta o CSS, não toca o DOM
- Variantes booleanas + valores dinâmicos = um componente, N aparências
- `attrs` para atributos HTML fixos ou computados
- Props locais + `theme` global = sistema de estilos completo
