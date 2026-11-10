# FE01-33 — Atividade: Box Model e Espaçamentos

## Objetivo da Atividade

Aplicar na prática a redefinição global para `box-sizing: border-box`, calcular espaçamentos internos e externos e criar cartões informativos com bordas estilizadas e centralização horizontal.

---

## Enunciado do Desafio

Construa o layout de um componente de cartão de plano de preços (`.pricing-card`) utilizando um arquivo `boxmodel.css`, cumprindo os seguintes pontos:

1. Reset do box model em todos os elementos (`*`) utilizando `box-sizing: border-box`, `margin: 0` e `padding: 0`.
2. Fundo geral da página (`body`) em cinza suave (`#f8fafc`) com fonte sem serifa.
3. Cartão de plano (`.pricing-card`):
   - Largura fixa de `320px`, centralizado horizontalmente na tela com margem automática (`margin: 60px auto`).
   - Preenchimento interno (`padding`) de `32px`.
   - Fundo branco (`#ffffff`).
   - Borda de `2px solid #3b82f6` (azul de destaque).
   - Cantos arredondados de `12px`.
4. Elementos internos do cartão:
   - Título do plano com margem inferior de `8px`.
   - Preço de destaque em tamanho grande com margem inferior de `20px`.
   - Lista de benefícios com marcadores removidos, onde cada item (`li`) possui preenchimento vertical de `8px` e borda inferior tracejada sutil (`1px dashed #e2e8f0`).
   - Botão de contratação com largura de `100%`, preenchimento interno de `12px`, sem borda, cantos arredondados de `6px` e margem superior de `24px`.

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
}

.pricing-card {
  width: 320px;
  margin: 60px auto;
  padding: 32px;
  background-color: #ffffff;
  border: 2px solid #3b82f6;
  border-radius: 12px;
}

.pricing-card h2 {
  font-size: 20px;
  color: #1e293b;
  margin-bottom: 8px;
}

.preco {
  font-size: 32px;
  font-weight: bold;
  color: #3b82f6;
  margin-bottom: 20px;
}

.beneficios {
  list-style: none;
  margin-bottom: 24px;
}

.beneficios li {
  padding: 8px 0;
  border-bottom: 1px dashed #e2e8f0;
  font-size: 14px;
}

.btn-assinar {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
```
