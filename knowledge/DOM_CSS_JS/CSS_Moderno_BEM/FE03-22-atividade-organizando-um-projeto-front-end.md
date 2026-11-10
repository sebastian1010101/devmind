# FE03-22 — Atividade: Organizando um Projeto Front-End

## Objetivo da Atividade

Organizar a estrutura de arquivos e diretórios de um projeto web, configurando os caminhos relativos corretos nas tags `<link>`, `<script>` e `<img>` sem quebrar o carregamento dos recursos.

---

## Enunciado do Desafio

Refatore um projeto que estava com todos os arquivos desorganizados na raiz, movendo-os para a estrutura modular padrão:

1. Mova as imagens para `src/assets/img/`.
2. Mova as folhas de estilo para `src/styles/` (com `reset.css`, `variables.css` e `index.css`).
3. Mova os scripts para `src/scripts/index.js`.
4. Mantenha o `index.html` na raiz do repositório.
5. Atualize todos os links de importação no cabeçalho e rodapé do HTML garantindo que a ordem de precedência do CSS seja respeitada (1º Reset, 2º Variáveis, 3º Estilos Próprios).

---

## Solução de Referência

### `index.html` (Na Raiz do Projeto)

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Kenzie Academy</title>

    <!-- 1. Reset CSS (deve vir sempre primeiro para zerar inconsistências) -->
    <link rel="stylesheet" href="./src/styles/reset.css">

    <!-- 2. Variáveis Globais (disponibiliza os tokens para os próximos arquivos) -->
    <link rel="stylesheet" href="./src/styles/variables.css">

    <!-- 3. Estilos dos Componentes e da Página -->
    <link rel="stylesheet" href="./src/styles/index.css">
  </head>
  <body>
    <header class="header">
      <!-- Caminho relativo navegando até os assets -->
      <img src="./src/assets/img/logo.svg" alt="Logotipo Kenzie" class="header__logo">
    </header>

    <main class="container">
      <h1>Bem-vindo ao Portal</h1>
    </main>

    <!-- Script JavaScript importado no final do body -->
    <script src="./src/scripts/index.js"></script>
  </body>
</html>
```
