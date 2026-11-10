# FE01-41 — Atividade: Menu de Navegação com Flexbox

## Objetivo da Atividade

Construir o componente mais comum e clássico de interfaces web modernas: um cabeçalho completo com logotipo à esquerda e menu de navegação alinhado à direita, aplicando `display: flex`, `justify-content: space-between` e `align-items: center`.

---

## O Padrão de Cabeçalho com Flexbox

Antes do Flexbox, alinhar o logotipo à esquerda e os botões à direita exigia cálculos com `float: left` e `float: right` somados a resets de `clear: both`.

Com Flexbox, a estrutura é direta:

```text
+---------------------------------------------------------------+
|  HEADER (display: flex; justify-content: space-between;)      |
|                                                               |
|  [ LOGO ]                    [ LINK 1 ]  [ LINK 2 ]  [ BOTÃO ]|
+---------------------------------------------------------------+
```

---

## Enunciado do Desafio

Crie a estrutura HTML e CSS de uma barra de navegação responsiva e elegante:

1. O `<header>` deve possuir fundo escuro (`#0f172a`), altura confortável e preenchimento lateral.
2. O container interno do cabeçalho deve usar `display: flex`, alinhamento vertical centralizado (`align-items: center`) e distribuição espaçada nas extremidades (`justify-content: space-between`).
3. O menu `<nav>` deve conter uma lista `<ul>` que também seja um container flex com espaçamento de `20px` entre os links.
4. Um botão de destaque de ação (*Call To Action - CTA*) no final do menu com estilo diferenciado.

---

## Solução de Referência

### `index.html`

```html
<header class="header-principal">
  <div class="nav-container">
    <a href="#" class="logo">Dev<span>Academy</span></a>

    <nav>
      <ul class="menu-lista">
        <li><a href="#" class="menu-link">Início</a></li>
        <li><a href="#" class="menu-link">Cursos</a></li>
        <li><a href="#" class="menu-link">Sobre</a></li>
        <li><a href="#" class="btn-destaque">Matricule-se</a></li>
      </ul>
    </nav>
  </div>
</header>
```

### `style.css`

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
}

.header-principal {
  background-color: #0f172a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  text-decoration: none;
}

.logo span {
  color: #38bdf8;
}

.menu-lista {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 20px;
}

.menu-link {
  color: #cbd5e1;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: color 0.2s;
}

.menu-link:hover {
  color: #38bdf8;
}

.btn-destaque {
  background-color: #38bdf8;
  color: #0f172a;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
  padding: 8px 18px;
  border-radius: 6px;
  transition: opacity 0.2s;
}

.btn-destaque:hover {
  opacity: 0.9;
}
```
