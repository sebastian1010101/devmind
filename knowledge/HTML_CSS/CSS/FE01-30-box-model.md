# FE01-30 — Box Model

## O Modelo de Caixa (Box Model)

No CSS, cada elemento renderizado na tela é tratado pelo motor do navegador como uma **caixa retangular**. O Box Model é o conceito fundamental que descreve as camadas que compõem essa caixa:

```text
+-------------------------------------------------------+
|                       MARGIN                          |
|  +-------------------------------------------------+  |
|  |                    BORDER                       |  |
|  |  +-------------------------------------------+  |  |
|  |  |                 PADDING                   |  |  |
|  |  |  +-------------------------------------+  |  |  |
|  |  |  |                                     |  |  |  |
|  |  |  |               CONTENT               |  |  |  |
|  |  |  |           (width x height)          |  |  |  |
|  |  |  |                                     |  |  |  |
|  |  |  +-------------------------------------+  |  |  |
|  |  +-------------------------------------------+  |  |
|  +-------------------------------------------------+  |
+-------------------------------------------------------+
```

---

## As Quatro Camadas do Box Model

1. **Content (Conteúdo):** a área central onde o texto, imagem ou mídia residem. Suas dimensões são controladas por `width` e `height`.
2. **Padding (Preenchimento Interno):** o espaço transparente entre o conteúdo e a borda da caixa.
3. **Border (Borda):** a linha que envolve o preenchimento e o conteúdo. Possui espessura, estilo e cor.
4. **Margin (Margem Externa):** o espaço transparente exterior à borda, responsável por afastar a caixa dos outros elementos ao redor.

---

## O Problema do `content-box` vs a Solução `border-box`

### Modelo Tradicional (`box-sizing: content-box` - Padrão do Navegador)
No modelo padrão, as dimensões `width` e `height` aplicam-se **apenas à área de conteúdo**. 

Se você define:
```css
.caixa {
  width: 200px;
  padding: 20px;
  border: 5px solid black;
}
```
A largura total final ocupada na tela será:
`200px (content) + 40px (padding esquerdo + direito) + 10px (bordas) = 250px`.
Isso frequentemente quebrava layouts na criação de colunas e grids.

### Modelo Moderno (`box-sizing: border-box` - Padrão da Indústria)
No modelo `border-box`, as propriedades `width` e `height` representam o **tamanho total da caixa visível** (incluindo conteúdo, padding e borda). O navegador comprime a área interna do conteúdo para manter as medidas exatas configuradas:

```css
* {
  box-sizing: border-box;
}
```
Com `border-box`, a caixa do exemplo anterior terá exatamente `200px` de largura total na tela.
