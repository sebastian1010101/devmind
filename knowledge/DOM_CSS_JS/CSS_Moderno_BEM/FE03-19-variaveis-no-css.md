# FE03-19 — Variáveis no CSS

## O que são Variáveis CSS (Custom Properties)?

As **Custom Properties** (comumente chamadas de Variáveis CSS) permitem armazenar valores reutilizáveis — como cores, fontes, sombras e espaçamentos — em um único lugar da folha de estilos.

Quando você precisa alterar a cor principal da marca de uma aplicação inteira, em vez de substituir dezenas de códigos hexadecimais espalhados por milhares de linhas de CSS, basta alterar o valor de **uma única variável**.

---

## Sintaxe de Declaração e Uso

### 1. Declaração no Escopo Global com `:root`

A pseudo-classe `:root` faz referência ao elemento raiz `<html>`, garantindo que as variáveis declaradas fiquem disponíveis para todos os elementos do documento:

```css
:root {
  /* Toda variável CSS DEVE começar com dois hifens -- */
  --cor-primaria: #2563eb;
  --cor-secundaria: #38bdf8;
  --cor-fundo: #f8fafc;
  --cor-texto: #1e293b;

  --fonte-principal: 'Inter', sans-serif;

  --espacamento-padrao: 1rem;
  --borda-suave: 8px;
  --sombra-card: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

### 2. Consumindo Variáveis com a Função `var()`

```css
body {
  font-family: var(--fonte-principal);
  background-color: var(--cor-fundo);
  color: var(--cor-texto);
}

.btn-destaque {
  background-color: var(--cor-primaria);
  border-radius: var(--borda-suave);
  padding: var(--espacamento-padrao);
}
```

---

## Valor de Contingência (Fallback)

A função `var()` aceita um segundo parâmetro opcional como valor de reserva caso a variável não tenha sido definida:

```css
.card {
  /* Se --cor-borda não existir, usa #e2e8f0 */
  border: 1px solid var(--cor-borda, #e2e8f0);
}
```

---

## Criando Temas Claros e Escuros com Variáveis

A grande vantagem de variáveis CSS é poder redefinir seus valores com base em classes ou preferências do usuário:

```css
:root {
  --bg-pagina: #ffffff;
  --texto-pagina: #0f172a;
}

/* Quando o body ganhar a classe dark-mode, as variáveis mudam automaticamente */
body.dark-mode {
  --bg-pagina: #0f172a;
  --texto-pagina: #f8fafc;
}

body {
  background-color: var(--bg-pagina);
  color: var(--texto-pagina);
}
```
