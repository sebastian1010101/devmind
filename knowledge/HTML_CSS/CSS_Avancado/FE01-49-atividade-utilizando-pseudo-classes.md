# FE01-49 — Atividade: Utilizando Pseudo Classes

## Objetivo da Atividade

Praticar a aplicação combinada de pseudo-classes de interação (`:hover`, `:focus`, `:active`), estruturais (`:first-child`, `:last-child`, `:nth-child`) e de formulários (`:checked`, `:disabled`) para construir uma interface viva e dinâmica.

---

## Enunciado do Desafio

Crie uma folha de estilos `interacoes.css` contemplando os seguintes elementos:

1. **Botão com Estados Completos:**
   - Estado normal: fundo azul `#2563eb`, texto branco, cantos de 6px.
   - `:hover`: escurece para `#1d4ed8` e desloca 2px para cima.
   - `:focus`: anel visível de foco (`outline: 2px solid #93c5fd; outline-offset: 2px`).
   - `:active`: afunda 1px (`transform: translateY(1px)`) simulando clique físico real.
2. **Tabela de Relatório Zebrada:**
   - Linhas pares (`tr:nth-child(even)`): fundo cinza muito suave (`#f8fafc`).
   - Linhas ímpares (`tr:nth-child(odd)`): fundo branco.
   - Destaque ao passar o mouse (`tbody tr:hover`): fundo suave `#e0e7ff`.
3. **Lista de Tarefas:**
   - O primeiro item (`li:first-child`): borda superior destacada.
   - O último item (`li:last-child`): sem borda inferior.
4. **Campo Desabilitado:**
   - `input:disabled`: cursor proibido (`cursor: not-allowed`), fundo cinza e opacidade reduzida a 0.6.

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
  padding: 32px;
  background-color: #ffffff;
  color: #1e293b;
}

/* 1. Botão com ciclo completo de estados */
.btn-interativo {
  display: inline-block;
  background-color: #2563eb;
  color: #ffffff;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-interativo:hover {
  background-color: #1d4ed8;
  transform: translateY(-2px);
}

.btn-interativo:focus {
  outline: 2px solid #93c5fd;
  outline-offset: 2px;
}

.btn-interativo:active {
  transform: translateY(1px);
}

/* 2. Tabela zebrada e interativa */
.tabela-dados {
  width: 100%;
  border-collapse: collapse;
  margin: 32px 0;
}

.tabela-dados th,
.tabela-dados td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.tabela-dados th {
  background-color: #0f172a;
  color: #ffffff;
}

.tabela-dados tbody tr:nth-child(odd) {
  background-color: #ffffff;
}

.tabela-dados tbody tr:nth-child(even) {
  background-color: #f8fafc;
}

.tabela-dados tbody tr:hover {
  background-color: #e0e7ff;
}

/* 3. Lista Estrutural */
.lista-tarefas {
  list-style: none;
  max-width: 400px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 32px;
}

.lista-tarefas li {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.lista-tarefas li:last-child {
  border-bottom: none;
}

/* 4. Campo Desabilitado */
.campo-desabilitado:disabled {
  background-color: #f1f5f9;
  color: #94a3b8;
  border: 1px solid #cbd5e1;
  cursor: not-allowed;
  opacity: 0.6;
}
```
