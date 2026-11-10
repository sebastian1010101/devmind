# FE01-45 — Atividade: Blog com Flexbox

## Objetivo da Atividade

Refatorar ou reconstruir a estrutura do projeto de Blog aplicando Flexbox para criar um layout com duas colunas dinâmicas (área principal de artigos + barra lateral fixa de widgets), com cabeçalho flexível e grade responsiva de posts secundários.

---

## Enunciado do Desafio

Construa a folha de estilos `blog-flexbox.css` atendendo aos seguintes pontos:

1. **Cabeçalho:** Logotipo e lista de links alinhados nas extremidades com `display: flex` e `justify-content: space-between`.
2. **Layout de Duas Colunas:** O elemento `.layout-grid` deve utilizar `display: flex` com espaçamento de `32px` (`gap: 32px`):
   - A coluna de artigos (`.coluna-principal`) deve crescer ocupando todo o espaço restante disponível usando a propriedade `flex: 1`.
   - A barra lateral (`.coluna-sidebar`) deve ter largura fixa e rígida de `320px` usando `flex: 0 0 320px`.
3. **Grade de Posts:** A seção de posts secundários dentro da coluna principal deve usar `display: flex` com `flex-wrap: wrap` e espaçamento uniforme de `16px`, organizando dois cards por linha.
4. **Alinhamento do Card:** Cada card de artigo deve ser um container flex vertical (`flex-direction: column`) para que o botão "Ler Mais" fique sempre alinhado na base inferior do card através de `margin-top: auto`.

---

## Solução de Referência

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background-color: #f8fafc;
  color: #1e293b;
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

/* 1. Header Flexível */
.header-blog {
  background-color: #0f172a;
  padding: 16px 0;
}

.nav-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 20px;
}

/* 2. Layout Principal de Duas Colunas */
.layout-grid {
  display: flex;
  gap: 32px;
  margin-top: 40px;
  margin-bottom: 40px;
}

.coluna-principal {
  flex: 1; /* Ocupa todo o espaço livre restante */
}

.coluna-sidebar {
  flex: 0 0 320px; /* Largura rígida de 320px sem encolher nem crescer */
}

/* 3. Grade de Posts em Flexbox */
.grade-posts {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.card-post {
  display: flex;
  flex-direction: column;
  flex: 1 1 calc(50% - 16px);
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
}

.card-post h3 {
  font-size: 18px;
  margin-bottom: 8px;
}

.card-post p {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 16px;
}

.card-post .btn-ler {
  margin-top: auto; /* Alinha o botão na base do card */
  align-self: flex-start;
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

/* Sidebar Box */
.widget {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}
```
