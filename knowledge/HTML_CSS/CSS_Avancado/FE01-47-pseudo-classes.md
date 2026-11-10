# FE01-47 — Pseudo Classes

## O que é uma Pseudo-Classe?

Uma **pseudo-classe** é uma palavra-chave adicionada a um seletor CSS (precedida por dois pontos `:`) que especifica um **estado especial** do elemento selecionado, ou seleciona elementos com base em sua posição na árvore do documento.

Sintaxe básica:
```css
seletor:pseudo-classe {
  propriedade: valor;
}
```

---

## Principais Categorias de Pseudo-Classes

### 1. Estados de Interação do Usuário

- `:hover`: disparado quando o cursor do mouse passa por cima do elemento.
- `:active`: ativado no exato milissegundo em que o elemento é clicado/pressionado.
- `:focus`: ativado quando o elemento recebe o foco do teclado ou clique (essencial em campos de formulário e botões acessíveis).
- `:visited`: estiliza links que o usuário já visitou anteriormente no histórico do navegador.

### 2. Estados de Formulários

- `:disabled`: seleciona campos ou botões que possuem o atributo `disabled`.
- `:checked`: seleciona radio buttons ou checkboxes que estão marcados no momento.
- `:required`: seleciona campos com preenchimento obrigatório.
- `:valid` / `:invalid`: estiliza campos conforme a validação nativa de formato (ex: e-mail correto vs incorreto).

### 3. Seleção Estrutural na Árvore DOM

- `:first-child`: seleciona o primeiro elemento filho do seu container pai.
- `:last-child`: seleciona o último elemento filho.
- `:nth-child(n)`: seleciona elementos baseados em fórmulas matemáticas ou contagens:
  - `:nth-child(2)`: seleciona o segundo filho.
  - `:nth-child(odd)` / `:nth-child(2n+1)`: seleciona todos os itens ímpares (ótimo para tabelas zebradas).
  - `:nth-child(even)` / `:nth-child(2n)`: seleciona todos os itens pares.
- `:not(seletor)`: pseudo-classe de negação, estiliza todos os elementos que **não** correspondem ao seletor interno:

```css
/* Estiliza todos os inputs, exceto o botão submit */
input:not([type="submit"]) {
  border: 1px solid #ccc;
  padding: 8px;
}
```
