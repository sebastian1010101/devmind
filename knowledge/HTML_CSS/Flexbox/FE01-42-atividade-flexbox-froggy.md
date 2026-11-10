# FE01-42 — Atividade: Flexbox Froggy

## O que é o Flexbox Froggy?

O **Flexbox Froggy** é um jogo educativo interativo online amplamente adotado no ensino de tecnologia (especialmente na metodologia Kenzie Academy) para fixar a intuição espacial das propriedades do Flexbox de forma lúdica.

O objetivo de cada nível é guiar o sapo (Froggy) até a sua respectiva folha de vitória-régia (*lilypad*) utilizando comandos CSS.

---

## Guia de Propriedades Utilizadas no Jogo

### 1. `justify-content` (Alinhamento Horizontal / Eixo Principal)
- `flex-start`: sapo alinhado à esquerda.
- `flex-end`: sapo movido para a direita extrema.
- `center`: sapo centralizado no meio do lago.
- `space-between`: sapos separados com espaço máximo entre si.
- `space-around`: sapos com margens iguais ao redor.
- `space-evenly`: espaçamento milimetricamente idêntico.

### 2. `align-items` (Alinhamento Vertical / Eixo Transversal)
- `flex-start`: topo do lago.
- `flex-end`: base inferior do lago.
- `center`: centro vertical.

### 3. `flex-direction` (Inversão e Rotação de Eixos)
- `row`: padrão horizontal (esquerda para a direita).
- `row-reverse`: inverte a ordem horizontal.
- `column`: transforma o eixo principal em vertical (cima para baixo).
- `column-reverse`: vertical invertido.

> **Regra de Ouro:** Quando `flex-direction: column` é aplicado, o papel das propriedades se inverte! O `justify-content` passa a controlar o eixo **vertical** e o `align-items` controla o eixo **horizontal**.

### 4. `order` (Ordem Individual do Item)
Por padrão, todos os itens flex possuem `order: 0`. Atribuir números negativos (ex: `order: -1`) ou positivos (ex: `order: 2`) move um item específico para a frente ou para trás sem alterar o código HTML.

### 5. `align-self` (Sobrescrita Individual de Alinhamento)
Permite que um único sapo tenha alinhamento diferente dos seus companheiros:

```css
#frog {
  align-self: flex-end; /* Apenas este sapo vai para o fundo */
}
```

### 6. `flex-wrap` e `align-content`
- `flex-wrap: wrap`: permite que sapos excedentes ocupem uma nova linha.
- `align-content`: alinha as linhas inteiras quando há múltiplas linhas com quebra.

---

## Dica de Estudo

Acesse e complete os 24 níveis em [flexboxfroggy.com](https://flexboxfroggy.com/#pt-br) para consolidar a memória muscular dos alinhamentos flexíveis.
