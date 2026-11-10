# FE01-20 — Textarea

## O Elemento `<textarea>`

Diferente do `<input type="text">`, que é restrito a uma única linha contínua, a tag `<textarea>` é projetada para **entradas de texto com múltiplas linhas**, preservando quebras de linha e permitindo redação de textos longos (como mensagens, avaliações, comentários e biografias).

```html
<label for="mensagem">Deixe sua mensagem:</label>
<textarea id="mensagem" name="mensagem"></textarea>
```

---

## Diferença Importante em Relação ao `<input>`

- A tag `<textarea>` **NÃO é um elemento autocontido**; ela possui tag de abertura e fechamento obrigatórias: `<textarea></textarea>`.
- **Não possui atributo `value`:** o texto padrão ou inicial deve ser escrito diretamente entre as tags de abertura e fechamento:

```html
<!-- Correto -->
<textarea id="bio" name="bio">Texto padrão inicial que já aparece digitado.</textarea>

<!-- Cuidado com espaços acidentais -->
<!-- Espaços e quebras de linha entre as tags são interpretados como caracteres reais -->
<textarea id="bio" name="bio">
</textarea>
```

---

## Principais Atributos de Configuração

| Atributo | Descrição |
| --- | --- |
| `rows` | Define a altura inicial do campo em quantidade de linhas visíveis (padrão do navegador costuma ser 2). |
| `cols` | Define a largura média visível em quantidade de colunas/caracteres por linha (padrão costuma ser 20). |
| `maxlength` | Limite máximo de caracteres que o usuário pode digitar. |
| `minlength` | Quantidade mínima de caracteres exigida para validação. |
| `placeholder` | Texto de instrução que desaparece assim que o usuário começa a digitar. |
| `required` | Torna o preenchimento obrigatório antes do envio do formulário. |

```html
<label for="feedback">Seu Feedback (máx. 300 caracteres):</label>
<textarea 
  id="feedback" 
  name="feedback" 
  rows="5" 
  cols="40" 
  maxlength="300"
  placeholder="Conte-nos como foi a sua experiência com a plataforma..."
  required
></textarea>
```

---

## Controle de Redimensionamento via CSS

Por padrão, a maioria dos navegadores exibe um controle no canto inferior direito que permite ao usuário redimensionar a área de texto livremente, podendo quebrar o layout da página.

Controla-se esse comportamento no CSS com a propriedade `resize`:

```css
textarea {
  /* Impede qualquer redimensionamento manual */
  resize: none;

  /* Ou permite apenas na vertical, protegendo a largura do layout */
  resize: vertical;
}
```
