# FE01-18 — Input radio

## O que é o `type="radio"`?

O `<input type="radio">` cria botões de seleção exclusiva (conhecidos como botões de rádio). São utilizados quando existe uma lista de duas ou mais opções mútuas, mas o usuário deve escolher **obrigatoriamente apenas uma única opção**.

Diferença entre Radio e Checkbox:

- **Checkbox:** escolha múltipla independente (o usuário pode marcar zero, uma ou várias caixas).
- **Radio:** escolha única mutuamente exclusiva (marcar uma opção desmarca automaticamente a anterior).

---

## O Papel Crucial do Atributo `name`

Para que os botões de rádio funcionem de forma mutuamente exclusiva, **todos os inputs do mesmo grupo devem compartilhar exatamente o mesmo atributo `name`**.

```html
<form>
  <p>Qual é o seu nível de escolaridade?</p>

  <div>
    <input type="radio" id="medio" name="escolaridade" value="ensino_medio">
    <label for="medio">Ensino Médio</label>
  </div>

  <div>
    <input type="radio" id="superior" name="escolaridade" value="ensino_superior">
    <label for="superior">Ensino Superior</label>
  </div>

  <div>
    <input type="radio" id="pos" name="escolaridade" value="pos_graduacao">
    <label for="pos">Pós-Graduação</label>
  </div>
</form>
```

Se o atributo `name` for diferente em cada um, o navegador os tratará como grupos separados e permitirá marcar todos ao mesmo tempo.

---

## O Atributo `value`

Como os botões de rádio não possuem texto digitado pelo usuário, o atributo `value` é **obrigatório**. É esse valor que será enviado ao servidor quando o formulário for submetido:

- Se o usuário escolher "Ensino Superior", o backend receberá o par:
  `escolaridade=ensino_superior`

---

## Atributo `checked`

Utilize o atributo booleano `checked` para indicar qual opção já deve vir pré-selecionada quando a página carregar:

```html
<input type="radio" id="opcao-padrao" name="tema" value="claro" checked>
<label for="opcao-padrao">Tema Claro (Padrão)</label>
```

---

## Agrupamento Semântico com `<fieldset>` e `<legend>`

Para garantir a melhor experiência em leitores de tela e manter o código semântico, grupos de rádios devem ser envolvidos por um `<fieldset>` com sua respectiva `<legend>`:

```html
<fieldset>
  <legend>Selecione a forma de pagamento:</legend>

  <input type="radio" id="pix" name="pagamento" value="pix" checked>
  <label for="pix">PIX</label>

  <input type="radio" id="cartao" name="pagamento" value="cartao">
  <label for="cartao">Cartão de Crédito</label>

  <input type="radio" id="boleto" name="pagamento" value="boleto">
  <label for="boleto">Boleto Bancário</label>
</fieldset>
```
