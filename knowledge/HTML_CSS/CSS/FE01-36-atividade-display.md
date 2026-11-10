# FE01-36 — Atividade: Display

## Objetivo da Atividade

Praticar a manipulação de propriedades de exibição (`display: block`, `display: inline-block`, `display: inline` e `display: none`), entendendo como transformar tags de bloco em elementos dispostos horizontalmente sem quebras indesejadas.

---

## Enunciado do Desafio

Construa a estilização de uma barra de navegação simples e um cartão de produto usando `display: inline-block`, cumprindo os critérios:

1. Uma lista não ordenada (`<ul>`) contendo itens de menu (`<li>`):
   - Os itens de lista (`<li>`), que por padrão são de bloco, devem ficar dispostos lado a lado na mesma linha usando `display: inline-block`.
   - Cada link (`<a>`) interno deve possuir preenchimento interno (`padding: 8px 16px`), fundo decorativo e bordas arredondadas.
2. Dois cartões de produtos (`.card-produto`):
   - Por padrão divs são blocos verticais. Transforme-os em `display: inline-block` com largura de `45%`, margem lateral de `2%` e alinhamento vertical no topo (`vertical-align: top`) para ficarem lado a lado.
3. Um elemento de aviso promocional (`.aviso-esgotado`) que precisa ser ocultado temporariamente da interface sem ser removido do HTML (`display: none`).

---

## Solução de Referência

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, sans-serif;
  padding: 24px;
}

/* Menu horizontal com inline-block */
.menu-navegacao {
  list-style: none;
  background-color: #24292f;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 32px;
}

.menu-navegacao li {
  display: inline-block;
  margin-right: 8px;
}

.menu-navegacao li a {
  display: inline-block;
  color: #ffffff;
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 4px;
}

.menu-navegacao li a:hover {
  background-color: #3f4752;
}

/* Cards lado a lado */
.card-produto {
  display: inline-block;
  width: 48%;
  margin-right: 2%;
  vertical-align: top;
  border: 1px solid #d0d7de;
  border-radius: 8px;
  padding: 16px;
  background: #ffffff;
}

/* Ocultação total do elemento no DOM visual */
.aviso-esgotado {
  display: none;
}
```
