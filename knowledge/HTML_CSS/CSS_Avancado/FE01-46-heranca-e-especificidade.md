# FE01-46 — Herança e Especificidade

## Herança no CSS

No CSS, certas propriedades aplicadas a um elemento pai são transmitidas automaticamente aos seus filhos e descendentes diretos.

- **Propriedades Herdadas:** quase todas ligadas à tipografia e texto: `color`, `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`, `text-align`.
- **Propriedades Não-Herdadas:** propriedades estruturais e do modelo de caixa: `margin`, `padding`, `border`, `background`, `width`, `height`, `position`, `display`.

### Palavras-Chave de Controle:
- `inherit`: força a herança do valor do elemento pai imediato.
- `initial`: redefine a propriedade para o valor padrão da especificação CSS.
- `unset`: age como `inherit` se a propriedade for naturalmente herdada, ou como `initial` se não for.

---

## Especificidade no CSS

Quando duas ou mais regras estilizam o mesmo elemento com propriedades conflitantes, o navegador calcula o peso de **especificidade** de cada seletor para decidir qual regra vence.

O cálculo pode ser compreendido como uma pontuação de 4 colunas `(A, B, C, D)`:

| Nível | Tipo de Seletor | Peso Explicativo | Exemplo |
| --- | --- | --- | --- |
| **A** | Estilo Inline | `1, 0, 0, 0` | `<h1 style="color: red;">` |
| **B** | IDs | `0, 1, 0, 0` | `#cabecalho` |
| **C** | Classes, Atributos e Pseudo-classes | `0, 0, 1, 0` | `.card`, `[type="text"]`, `:hover` |
| **D** | Elementos (Tags) e Pseudo-elementos | `0, 0, 0, 1` | `h1`, `p`, `div`, `::before` |

*O Seletor Universal (`*`) possui especificidade nula `(0, 0, 0, 0)`.*

---

## Exemplos Práticos de Comparação

1. `p` &rarr; `(0, 0, 0, 1)`
2. `.destaque` &rarr; `(0, 0, 1, 0)` &rarr; **Vence o seletor `p`**
3. `p.destaque` &rarr; `(0, 0, 1, 1)` &rarr; **Vence `.destaque` puro**
4. `#titulo-principal` &rarr; `(0, 1, 0, 0)` &rarr; **Vence qualquer combinação de classes sem ID**

---

## O Recurso Extremo: `!important`

Adicionar `!important` a uma declaração faz com que ela ignore a cascata e vença qualquer outro cálculo de especificidade regular:

```css
p {
  color: blue !important;
}
```

> **Atenção:** Evite o uso de `!important`. Ele quebra a natureza natural da cascata e gera débitos técnicos difíceis de depurar. Prefira organizar seus seletores com classes semânticas.
