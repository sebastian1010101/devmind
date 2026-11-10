# FE03-23 — Importando Arquivos no CSS

## A Diretiva `@import`

O CSS oferece uma diretiva nativa chamada `@import`, que permite carregar um arquivo de estilo de dentro de outro arquivo CSS:

```css
/* Dentro de style.css */
@import url("./reset.css");
@import url("./variables.css");
@import url("./components/buttons.css");
```

---

## Regra de Sintaxe Obrigatória do `@import`

A diretiva `@import` **deve obrigatoriamente estar na primeiríssima linha do arquivo CSS**, antes de qualquer outra regra ou declaração de estilo. Qualquer código escrito antes de um `@import` faz com que o navegador ignore a importação.

---

## Vantagens e Cuidados de Performance

### Vantagens:
- **HTML Limpo:** o documento `index.html` precisa de apenas uma única tag `<link rel="stylesheet" href="src/styles/index.css">` no `<head>`, enquanto o arquivo `index.css` centraliza e orquestra a importação de todos os submódulos de estilo.

### Cuidados de Performance em Produção:
- Cada declaração `@import` gera uma requisição HTTP sequencial adicional (*bloqueio de renderização em cascata*): o navegador precisa baixar o primeiro CSS, lê-lo, descobrir que há outros arquivos importados e só então disparar as requisições secundárias.
- Em projetos grandes sem ferramentas de compilação (*bundlers* como Vite ou Webpack), vincular múltiplos arquivos via `<link>` no HTML é ligeiramente mais veloz, pois o navegador dispara os downloads em paralelo simultaneamente.
- Em ambientes modernos de desenvolvimento com bundlers, o `@import` é resolvido e mesclado em um único arquivo final minificado durante o processo de *build*.
