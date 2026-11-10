# FE03-26 — Position

## O Modelo de Posicionamento no CSS

Por padrão, todos os elementos em uma página web seguem o **fluxo normal do documento** (*Normal Flow*): elementos em bloco empilham-se verticalmente de cima para baixo e elementos em linha alinham-se lado a lado da esquerda para a direita.

A propriedade `position` permite alterar essas regras naturais para criar sobreposições de camadas, fixar barras de navegação ou ancorar elementos em cantos específicos da tela.

---

## Os Cinco Valores da Propriedade `position`

| Valor | Sai do Fluxo Normal? | Ponto de Referência | Efeito de `top`/`left` |
| --- | --- | --- | --- |
| `static` (Padrão) | Não | Fluxo natural do HTML | Nenhum |
| `relative` | Não | A sua própria posição original | Desloca visualmente |
| `absolute` | **Sim** | O ancestral posicionado mais próximo | Move relativamente ao pai |
| `fixed` | **Sim** | A janela de exibição (*viewport*) | Fixo mesmo ao rolar |
| `sticky` | Não (até o limite) | O container pai e o scroll | Gruda ao atingir o offset |

---

## As Propriedades Direcionais (Offsets)

Quando um elemento possui `position` diferente de `static`, quatro propriedades passam a ter efeito:
- `top`: distância em relação ao topo.
- `bottom`: distância em relação à base.
- `left`: distância em relação à esquerda.
- `right`: distância em relação à direita.

```css
.badge {
  position: absolute;
  top: 10px;
  right: 15px;
}
```
