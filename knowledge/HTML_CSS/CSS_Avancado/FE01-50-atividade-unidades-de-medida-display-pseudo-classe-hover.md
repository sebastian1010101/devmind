# FE01-50 — Atividade: Unidades de Medida, Display, Pseudo Classe (hover)

## Objetivo da Atividade

Consolidar o domínio de arquitetura visual moderna: combinar unidades de medida relativas e fluidas (`rem`, `%`), sistemas de exibição (`display: flex`) e efeitos visuais refinados acionados por pseudo-classes `:hover` para criar um painel de estatísticas (*dashboard cards*).

---

## Enunciado do Desafio

Desenvolva a estilização de uma grade com três cartões métricos de painel (`.stats-grid`), cumprindo os requisitos:

1. **Tipografia e Espaçamentos em `rem`:**
   - Tamanho base no body: `1rem` (16px).
   - Títulos em `1.25rem` (20px), métricas de números grandes em `2rem` (32px) com peso `bold`.
   - Espaçamentos e paddings declarados com múltiplos de rem (ex: `1rem`, `1.5rem`).
2. **Disposição Flexível (`display: flex`):**
   - O container `.stats-grid` deve utilizar `display: flex`, espaçamento entre cards de `1.5rem` (`gap: 1.5rem`) e permitir quebra para novas linhas quando necessário (`flex-wrap: wrap`).
   - Cada card (`.stat-card`) deve ocupar no mínimo `16rem` de largura base e crescer proporcionalmente (`flex: 1 1 16rem`).
3. **Efeitos Visuais Interativos com `:hover`:**
   - No estado padrão: borda de `1px solid #e2e8f0`, fundo branco e transição suave de `0.3s`.
   - No estado `:hover`:
     - O card deve se erguer suavemente `transform: translateY(-4px)`.
     - Ganhar uma sombra marcante (`box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1)`).
     - Alterar a cor da borda para o azul de destaque (`border-color: #3b82f6`).

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
  padding: 2rem;
}

.stats-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  max-width: 75rem; /* 1200px */
  margin: 0 auto;
}

.stat-card {
  flex: 1 1 16rem;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: #3b82f6;
  box-shadow: 0 12px 20px -5px rgba(59, 130, 246, 0.15);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.stat-titulo {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-valor {
  font-size: 2rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.stat-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  background-color: #dcfce7;
  color: #15803d;
}
```
