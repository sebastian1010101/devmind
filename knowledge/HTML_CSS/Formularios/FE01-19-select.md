# FE01-19 — Select

## O Elemento `<select>`

A tag `<select>` cria um menu suspenso de opções (*dropdown*). É a escolha ideal para seleção de uma ou mais opções quando a lista é extensa (como estados, países ou categorias), economizando espaço visual na tela se comparado a uma longa sequência de botões de rádio.

---

## Estrutura Básica com `<option>`

O container `<select>` envolve múltiplos elementos filhos `<option>`:

```html
<label for="estado">Selecione seu Estado:</label>
<select id="estado" name="estado" required>
  <option value="" disabled selected>-- Escolha um estado --</option>
  <option value="PR">Paraná</option>
  <option value="SP">São Paulo</option>
  <option value="RJ">Rio de Janeiro</option>
  <option value="MG">Minas Gerais</option>
</select>
```

- **Texto entre `<option>` e `</option>`:** o que o usuário visualiza na interface gráfica.
- **Atributo `value`:** o valor real enviado ao backend. Se o `value` for omitido, o navegador enviará o próprio texto visível.
- **Opção padrão desabilitada:** `<option value="" disabled selected>` serve como instrução de preenchimento e impede que seja considerada válida em campos com `required`.

---

## Agrupando Opções com `<optgroup>`

Para listas longas e hierárquicas, a tag `<optgroup>` permite organizar as opções em blocos temáticos com um rótulo (`label`):

```html
<label for="veiculo">Escolha um modelo de veículo:</label>
<select id="veiculo" name="veiculo">
  <optgroup label="Carros Hatch">
    <option value="onix">Chevrolet Onix</option>
    <option value="hb20">Hyundai HB20</option>
    <option value="polo">Volkswagen Polo</option>
  </optgroup>

  <optgroup label="SUVs">
    <option value="creta">Hyundai Creta</option>
    <option value="tcross">Volkswagen T-Cross</option>
    <option value="tracker">Chevrolet Tracker</option>
  </optgroup>
</select>
```

---

## Seleção Múltipla com o Atributo `multiple`

Por padrão, o `<select>` permite a escolha de apenas um item. Com o atributo booleano `multiple`, o usuário pode selecionar vários itens pressionando `Ctrl` (Windows/Linux) ou `Cmd` (macOS):

```html
<label for="habilidades">Habilidades técnicas (selecione várias):</label>
<select id="habilidades" name="habilidades" multiple size="4">
  <option value="html">HTML5</option>
  <option value="css">CSS3</option>
  <option value="js">JavaScript</option>
  <option value="react">React</option>
  <option value="node">Node.js</option>
</select>
```

- `size`: define quantas opções ficam visíveis simultaneamente sem precisar rolar o menu.
