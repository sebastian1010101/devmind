# FE03-20 — Atividade: Figma e Variáveis CSS

## Objetivo da Atividade

Extrair os *Design Tokens* (paleta de cores, tipografia, raios de borda e sombras) de uma especificação visual de layout e implementá-los como variáveis em um arquivo CSS dedicado.

---

## Enunciado do Desafio

Dado o guia de estilos extraído do Figma para a nova interface de um dashboard financeiro:

- Cor Primária da Marca: Azul Cobalto (`#1d4ed8`)
- Cor de Destaque / Ação: Verde Esmeralda (`#10b981`)
- Fundo Neutro: Cinza Claro (`#f1f5f9`)
- Fundo dos Cards: Branco Puro (`#ffffff`)
- Texto Principal: Preto Grafite (`#0f172a`)
- Texto Secundário: Cinza Médio (`#64748b`)
- Tipografia: `"Poppins", system-ui, sans-serif`
- Raio de Borda Padrão: `12px`
- Raio de Borda de Botões: `6px`

Crie o arquivo `theme.css` com a declaração dessas propriedades no `:root` e estilize um cartão de métrica financeira utilizando exclusivamente as variáveis criadas via `var()`.

---

## Solução de Referência

```css
/* 1. Definição do Design System no :root */
:root {
  /* Cores */
  --color-primary: #1d4ed8;
  --color-accent: #10b981;
  --color-bg: #f1f5f9;
  --color-card: #ffffff;
  --color-text-main: #0f172a;
  --color-text-muted: #64748b;
  --color-border: #e2e8f0;

  /* Tipografia */
  --font-family-base: "Poppins", system-ui, sans-serif;

  /* Espaçamentos e Raios */
  --radius-card: 12px;
  --radius-btn: 6px;
  --spacing-base: 1.5rem;
  --shadow-elevation: 0 10px 15px -3px rgba(15, 23, 42, 0.08);
}

/* 2. Aplicação das variáveis na página */
body {
  font-family: var(--font-family-base);
  background-color: var(--color-bg);
  color: var(--color-text-main);
  padding: var(--spacing-base);
}

.metric-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-elevation);
  padding: var(--spacing-base);
  max-width: 340px;
}

.metric-card__title {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.metric-card__value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-main);
  margin-bottom: 1rem;
}

.metric-card__btn {
  background-color: var(--color-accent);
  color: #ffffff;
  border: none;
  border-radius: var(--radius-btn);
  padding: 0.625rem 1.25rem;
  font-weight: 600;
  cursor: pointer;
}
```
