# FE01-39 — Introdução ao Flexbox

## O que é o Flexbox?

O **Flexible Box Layout Module** (Flexbox) é um modelo de layout unidimensional criado no CSS3 para distribuir espaço e alinhar itens dentro de um container de maneira eficiente e previsível, mesmo quando os tamanhos dos elementos são dinâmicos ou desconhecidos.

Antes do Flexbox, o alinhamento horizontal e a distribuição de colunas dependiam de truques com `float`, `clear` e cálculos manuais de `inline-block`. O Flexbox resolveu esses problemas definitivamente.

---

## Conceitos Fundamentais: Container vs Itens

O Flexbox funciona com base em dois papéis distintos:

```text
+-------------------------------------------------------+
|  FLEX CONTAINER (display: flex)                       |
|                                                       |
|  +----------------+ +----------------+ +-----------+  |
|  |   FLEX ITEM    | |   FLEX ITEM    | | FLEX ITEM |  |
|  +----------------+ +----------------+ +-----------+  |
+-------------------------------------------------------+
```

1. **Flex Container (Pai):** o elemento onde você declara `display: flex` ou `display: inline-flex`. Ele passa a comandar as regras de alinhamento, direção e espaçamento.
2. **Flex Items (Filhos Diretos):** todos os elementos filhos imediatos do container tornam-se automaticamente itens flexíveis.

---

## Os Dois Eixos do Flexbox

Toda a lógica de posicionamento do Flexbox gira em torno de dois eixos perpendiculares:

1. **Eixo Principal (Main Axis):** o eixo primário ao longo do qual os itens flexíveis são distribuídos. Por padrão, ele corre na horizontal da esquerda para a direita (`row`).
2. **Eixo Transversal (Cross Axis):** o eixo perpendicular ao eixo principal. Se o eixo principal for horizontal, o transversal será vertical de cima para baixo.

---

## Propriedades Iniciais do Flex Container

### 1. `display: flex`

Ativa o contexto flexível no elemento pai.

```css
.container {
  display: flex;
}
```

### 2. `flex-direction`

Define a direção do eixo principal (Main Axis):

- `row` (Padrão): itens dispostos horizontalmente, da esquerda para a direita.
- `row-reverse`: horizontal, da direita para a esquerda.
- `column`: vertical, de cima para baixo.
- `column-reverse`: vertical, de baixo para cima.

### 3. `gap`

Define o espaçamento uniforme entre os itens flexíveis sem a necessidade de recorrer a margens manuais:

```css
.container {
  display: flex;
  gap: 16px; /* 16px entre cada elemento flexível */
}
```
