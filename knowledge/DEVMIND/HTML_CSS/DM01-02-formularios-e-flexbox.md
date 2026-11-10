# DM01-02 — Formulários acessíveis e linhas flexíveis

## Associar rótulo e campo

Dê um identificador único ao campo e use o mesmo valor em `for` no rótulo. Assim o navegador associa o texto ao campo e, por exemplo, clicar em “Cidade” coloca o foco no controle. Mantenha o rótulo visível durante o preenchimento.

```html
<label for="city">Cidade</label>
<input id="city" name="city" autocomplete="address-level2">
```

## Deixar controles quebrarem linha com Flexbox

Para um grupo de controles que precisa se adaptar à largura da tela, aplique `display: flex`, `flex-wrap: wrap` e `gap: 0.75rem` ao contêiner. Em telas estreitas, os itens podem passar à próxima linha, mantendo espaçamento. Se os itens também precisarem crescer, defina `flex: 1 1 14rem` neles e teste a largura mínima do conteúdo.

Referências [HTML Standard](https://html.spec.whatwg.org/multipage/forms.html#the-label-element) e [CSS Flexbox Level 1](https://www.w3.org/TR/css-flexbox-1/).
