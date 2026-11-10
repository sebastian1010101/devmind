# FE01-40 — Atividade: Flexbox

## Objetivo da Atividade

Praticar as propriedades centrais de alinhamento do Flexbox nos dois eixos: `justify-content` (alinhamento no eixo principal), `align-items` (alinhamento no eixo transversal) e `flex-wrap` (quebra de linha).

---

## Conceito das Propriedades de Alinhamento

### 1. `justify-content` (Eixo Principal)

Controla como os itens são distribuídos ao longo do eixo principal:

- `flex-start` (padrão): alinhados no início do container.
- `flex-end`: alinhados no final do container.
- `center`: centralizados no container.
- `space-between`: primeiro item no início, último no fim e espaço restante dividido igualmente entre eles.
- `space-around`: espaçamento igual ao redor de cada item.
- `space-evenly`: espaçamento milimetricamente idêntico entre todos os itens e as bordas.

### 2. `align-items` (Eixo Transversal)

Controla o alinhamento dos itens no eixo perpendicular:

- `stretch` (padrão): estica os itens para preencher toda a altura do container (se altura não for fixa).
- `center`: centraliza os itens verticalmente.
- `flex-start`: alinha ao topo do container.
- `flex-end`: alinha à base do container.

### 3. `flex-wrap` (Controle de Quebra)

- `nowrap` (padrão): todos os itens são espremidos em uma única linha.
- `wrap`: permite que os itens quebrem para a próxima linha quando não houver espaço suficiente.

---

## Enunciado do Desafio

Crie um layout de vitrine de catálogo (`.catalogo`) onde:

1. O container utilize `display: flex`, com quebra de linhas ativada (`flex-wrap: wrap`) e espaçamento de `24px` entre os produtos (`gap: 24px`).
2. Os cards de produtos devem ficar distribuídos com espaçamento uniforme usando `justify-content: space-between`.
3. Cada card (`.card-produto`) deve ter largura base calculada para exibir 3 produtos por linha em telas médias.
4. O conteúdo interno de cada card deve ser outro container flex vertical (`flex-direction: column`) com alinhamento de texto e botão centralizados.

---

## Solução de Referência

```css
.catalogo {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
}

.card-produto {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: calc(33.333% - 16px);
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
}

.card-produto img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 12px;
}

.card-produto h3 {
  font-size: 18px;
  margin-bottom: 8px;
  text-align: center;
}

.card-produto .preco {
  color: #2563eb;
  font-weight: bold;
  font-size: 20px;
  margin-bottom: 16px;
}

.card-produto button {
  margin-top: auto; /* Empurra o botão sempre para o rodapé do card */
  padding: 10px 20px;
  background-color: #2563eb;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
}
```
