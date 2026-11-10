# FE03-27 — Position: Absolute e Relative

## A Dupla Inseparável: Relative no Pai, Absolute no Filho

A técnica de posicionamento mais utilizada no CSS para criar selos (*badges*), ícones sobrepostos e botões de fechar consiste em combinar:

1. **Elemento Pai com `position: relative`:** atua como a **moldura de referência** delimitadora, sem sair do fluxo normal da página.
2. **Elemento Filho com `position: absolute`:** é retirado do fluxo normal e se move livremente dentro das quatro bordas do pai.

---

## O Problema Sem o Pai `relative`

Se você aplicar `position: absolute` em um filho e nenhum dos seus elementos pais tiver `position` configurado, o elemento filho usará a **página inteira (`<html>`)** como referência, voando para o canto do navegador.

---

## Exemplo Prático: Card de Produto com Badge de Desconto

```html
<article class="card-produto">
  <span class="card-produto__badge">-20% OFF</span>
  <img src="tenis.jpg" alt="Tênis Esportivo">
  <h3>Tênis Corrida Pro</h3>
</article>
```

```css
/* PAI: cria a âncora de referência */
.card-produto {
  position: relative;
  width: 280px;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e2e8f0;
}

/* FILHO: posicionado exatamente no canto superior direito do pai */
.card-produto__badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background-color: #ef4444; /* Vermelho vibrante */
  color: #ffffff;
  font-size: 12px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
}
```

---

## Centralização Perfeita com Absolute e Transform

Uma técnica consagrada para centralizar qualquer elemento dentro do seu pai relativo sem depender de Flexbox:

```css
.elemento-centralizado {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```
