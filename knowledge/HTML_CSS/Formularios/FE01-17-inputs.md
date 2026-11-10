# FE01-17 — Inputs

## A Tag `<input>`

A tag `<input>` é o elemento de entrada de dados mais flexível e utilizado no HTML. Trata-se de um elemento autocontido (*void element*) cujo comportamento e interface gráfica mudam de acordo com o valor atribuído ao seu atributo `type`.

```html
<input type="tipo_do_campo" name="identificador" id="identificador">
```

---

## Tipos Fundamentais de `type`

| `type` | Finalidade | Comportamento Específico |
| --- | --- | --- |
| `text` | Texto simples de uma única linha (padrão quando omitido). | Aceita qualquer caractere textual. |
| `password` | Senhas e dados confidenciais. | Oculta os caracteres digitados substituindo-os por pontos ou asteriscos. |
| `email` | Endereços de e-mail. | Valida a presença do caractere `@` e domínio no momento do envio; ativa teclado com `@` em dispositivos móveis. |
| `number` | Valores numéricos. | Adiciona setas de incremento/decremento e restringe entradas não numéricas. Suporta atributos `min`, `max` e `step`. |
| `tel` | Números de telefone. | Ativa o teclado numérico de discagem em aparelhos celulares (não realiza validação automática de formato). |
| `url` | Endereços web completos. | Exige formato válido de URL (com protocolo `http://` ou `https://`). |
| `date` | Seleção de data. | Abre um seletor visual nativo de calendário com suporte a ano, mês e dia. |
| `checkbox` | Caixa de seleção binária (marcado / desmarcado). | Usado para opções independentes onde o usuário pode escolher múltiplas alternativas simultaneamente. |
| `hidden` | Campo invisível na interface. | Armazena dados que precisam ser enviados ao backend sem que o usuário visualize ou edite diretamente (ex: IDs de sessão, tokens CSRF). |
| `submit` | Botão de envio do formulário. | Dispara a submissão dos dados preenchidos no `<form>`. |

---

## Atributos Essenciais de Validação e Usabilidade

```html
<input 
  type="text" 
  name="usuario" 
  id="usuario"
  placeholder="Digite seu nome de usuário"
  required
  minlength="3"
  maxlength="20"
  autocomplete="username"
>
```

- `placeholder`: texto de ajuda provisório exibido em cinza claro antes da digitação. **Nunca deve substituir a `<label>`**.
- `required`: atributo booleano que impede o envio do formulário se o campo estiver vazio.
- `minlength` e `maxlength`: limitam o número mínimo e máximo de caracteres permitidos.
- `min`, `max` e `step`: controlam o intervalo e o passo de incremento em inputs do tipo `number` e `date`.
- `disabled`: desabilita o campo para edição e exclui seu valor do envio ao backend.
- `readonly`: impede a edição pelo usuário, porém o dado ainda é submetido normalmente no envio.
- `value`: define o valor padrão inicial do campo.
