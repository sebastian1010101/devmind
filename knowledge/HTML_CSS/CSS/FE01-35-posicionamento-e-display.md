# FE01-35 — Posicionamento e Display

## A Propriedade `position` no CSS

A propriedade `position` determina como um elemento é calculado no fluxo do documento e permite deslocá-lo usando as propriedades direcionais `top`, `right`, `bottom` e `left` (e o índice de profundidade `z-index`).

---

## 1. `position: static` (Padrão)

O comportamento normal do fluxo HTML. O elemento é posicionado onde a ordem natural do código o coloca. As propriedades `top`, `right`, `bottom`, `left` e `z-index` **não têm nenhum efeito**.

---

## 2. `position: relative`

O elemento permanece no fluxo normal, ocupando seu espaço original, mas pode ser deslocado visualmente em relação à **sua própria posição original**:

```css
.card-deslocado {
  position: relative;
  top: 10px;  /* Move 10px para baixo da sua posição original */
  left: 20px; /* Move 20px para a direita */
}
```

- Os elementos vizinhos **não preenchem** o espaço original deixado para trás.
- É muito utilizado como ponto de ancoragem (*referência*) para elementos com `position: absolute` aninhados dentro dele.

---

## 3. `position: absolute`

O elemento é **removido totalmente do fluxo normal do documento**. Os elementos vizinhos agem como se ele não existisse:

```css
.badge-notificacao {
  position: absolute;
  top: -5px;
  right: -5px;
}
```

- Ele se posiciona em relação ao **ancestral mais próximo que tenha `position` diferente de `static`** (geralmente um pai com `position: relative`).
- Se nenhum ancestral tiver posição definida, ele se posiciona em relação ao elemento raiz `<html>` (a página inteira).

---

## 4. `position: fixed`

Também é removido do fluxo normal, mas se posiciona em relação direta à **janela de visualização (viewport)** do navegador:

```css
.cabecalho-fixo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}
```

- Permanece fixo no mesmo lugar da tela mesmo quando o usuário rola a página (muito comum em barras de navegação persistentes e botões de chat flutuantes).

---

## 5. `position: sticky`

Um híbrido inteligente entre `relative` e `fixed`:

```css
.indice-lateral {
  position: sticky;
  top: 20px;
}
```

- Age como `relative` até que a rolagem da página atinja o limite declarado (`top: 20px`), momento em que passa a se comportar como fixo (*gruda* na tela) enquanto durar o seu container pai.

---

## A Camada de Profundidade: `z-index`

Controla a ordem de sobreposição no eixo Z (para frente e para trás). Funciona apenas em elementos com `position` diferente de `static`:

- Valores maiores ficam sobrepostos na frente de valores menores: `z-index: 10` fica acima de `z-index: 1`.
