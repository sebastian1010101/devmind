# FE01-16 — Introdução a Formulários

## O que é um Formulário HTML?

Formulários são os componentes essenciais para **coleta de dados e interação ativa do usuário** em páginas web. Enquanto textos e imagens transmitem informações do servidor para o usuário, os formulários enviam informações do usuário de volta para o servidor (como cadastros, logins, buscas e feedbacks).

Todo formulário em HTML é envolvido pela tag semântica `<form>`.

```html
<form action="/processar-dados" method="POST">
  <!-- Campos do formulário ficam aqui -->
</form>
```

---

## Principais Atributos da Tag `<form>`

### 1. `action`

- Define a URL ou rota no servidor para onde os dados preenchidos serão enviados após a submissão.
- Se omitido ou deixado vazio (`action=""`), os dados são submetidos para a própria página atual.

### 2. `method`

Define o método de requisição HTTP utilizado para enviar os dados:

| Método | Funcionamento | Quando Usar |
| --- | --- | --- |
| `GET` (Padrão) | Anexa os dados diretamente na URL em formato de query string: `/busca?termo=html&categoria=livros`. Limite de caracteres e visível no histórico do navegador. | Buscas, filtros e consultas onde não há dados sensíveis e a URL pode ser compartilhada. |
| `POST` | Envia os dados encapsulados no corpo da requisição (*body*), ocultos da URL. Não há limite restrito de tamanho. | Criação de cadastros, logins, senhas, transações financeiras e envio de arquivos. |

### 3. `enctype`

Especifica como os dados do formulário devem ser codificados ao serem enviados via `POST`:

- `application/x-www-form-urlencoded`: formato padrão de texto.
- `multipart/form-data`: **obrigatório** sempre que houver upload de arquivos (`<input type="file">`).

---

## A Importância da Tag `<label>`

A tag `<label>` representa a legenda textual de um controle de formulário. É crucial por dois motivos:

1. **Acessibilidade:** leitores de tela leem o texto do `<label>` quando o usuário foca no campo correspondente.
2. **Usabilidade:** clicar no texto do `<label>` move automaticamente o foco (cursor) para o campo associado.

### Como associar Label e Input

**Abordagem recomendada (via atributo `for` e `id`):**

```html
<label for="nome-usuario">Nome Completo:</label>
<input type="text" id="nome-usuario" name="nome">
```

> O valor do atributo `for` na `<label>` deve ser idêntico ao valor do `id` no `<input>`.

**Abordagem aninhada:**

```html
<label>
  E-mail:
  <input type="email" name="email">
</label>
```

---

## O Papel do Atributo `name`

Sem o atributo `name`, o dado preenchido no campo **não é enviado** para o servidor na submissão. O atributo `name` funciona como a chave (*key*) no par chave-valor recebido no backend:

```html
<input type="text" id="campo-cidade" name="cidade">
<!-- No envio GET vira: ?cidade=Curitiba -->
```
