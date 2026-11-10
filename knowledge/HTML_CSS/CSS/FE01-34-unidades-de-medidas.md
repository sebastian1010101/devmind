# FE01-34 — Unidades de Medidas

## Categorias de Unidades no CSS

As unidades de medida no CSS são divididas entre **absolutas** e **relativas**:

---

## 1. Unidades Absolutas

São fixas e não mudam em função de outros elementos ou do tamanho da tela:

- **`px` (Pixels):** a unidade absoluta mais utilizada. 1px corresponde a um ponto na grade do monitor (pixel do CSS). Ideal para bordas finas, sombras e medidas que devem ser estritamente fixas.

---

## 2. Unidades Relativas à Tipografia

Adaptam-se dinamicamente às preferências de tamanho de fonte do usuário (essenciais para acessibilidade):

### `rem` (Root EM) — A Mais Recomendada para Espaçamento e Tipografia
- É calculada em relação ao tamanho da fonte do **elemento raiz** (`<html>`).
- Por padrão, a maioria dos navegadores adota `16px` como fonte raiz.
  - `1rem = 16px`
  - `1.5rem = 24px`
  - `2rem = 32px`
  - `0.5rem = 8px`
- Se um usuário com deficiência visual aumentar o tamanho de fonte padrão nas preferências do navegador para 24px, todo o layout em `rem` escala proporcionalmente de forma perfeita.

### `em`
- É calculada em relação ao tamanho da fonte do **próprio elemento** (ou do elemento pai imediato).
- Pode acumular efeito multiplicativo quando aninhada, tornando o cálculo complexo. Ótima para preenchimentos internos de botões que devem crescer junto com o texto do botão.

---

## 3. Unidades Relativas à Viewport (Janela de Exibição)

Calculadas em porcentagem da área visível do navegador:

- **`vw` (Viewport Width):** 1vw = 1% da largura total da janela visível.
- **`vh` (Viewport Height):** 1vh = 1% da altura total da janela visível (`100vh` preenche a tela inteira).
- **`%` (Porcentagem):** relativa ao tamanho do **elemento pai direto** (não da janela inteira).

---

## Resumo de Boas Práticas

| Propriedade | Unidade Recomendada | Motivo |
| --- | --- | --- |
| Tamanho de Fontes (`font-size`) | `rem` | Respeita a acessibilidade e preferências do usuário. |
| Espaçamentos (`margin`, `padding`) | `rem` ou `px` | `rem` garante escalabilidade harmônica; `px` garante controle fino. |
| Bordas (`border-width`) | `px` | Bordas de 1px ou 2px não devem se multiplicar excessivamente. |
| Larguras de Container (`max-width`) | `rem`, `%`, `vw` | Proporciona fluidez responsiva em diferentes tamanhos de tela. |
