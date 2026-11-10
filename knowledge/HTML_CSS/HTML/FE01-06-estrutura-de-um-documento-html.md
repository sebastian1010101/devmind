# FE01-06 — Estrutura de um Documento HTML

## Estrutura Básica Padrão

Todo documento HTML5 bem formado segue a estrutura mínima abaixo:

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Título da Página</title>
  </head>
  <body>
    <h1>Olá, mundo!</h1>
    <p>Este é meu primeiro documento HTML estruturado.</p>
  </body>
</html>
```

---

## Detalhamento das Partes

### 1. `<!DOCTYPE html>`

- Declaração que informa ao navegador que o documento utiliza a versão **HTML5**.
- Deve ser a primeiríssima linha do arquivo, antes de qualquer outra tag.
- Evita que o navegador entre no modo de compatibilidade legado (*quirks mode*).

### 2. `<html lang="pt-BR">`

- O elemento raiz (*root element*) que envolve todo o conteúdo da página.
- O atributo `lang="pt-BR"` informa o idioma principal do documento, auxiliando leitores de tela e motores de busca.

### 3. `<head>`

- Contém os **metadados** da página: dados sobre a página que não aparecem diretamente na área de exibição visual.
- **`<meta charset="UTF-8">`**: define a codificação de caracteres como UTF-8, garantindo suporte correto a acentos, cedilha e caracteres especiais.
- **`<meta name="viewport" content="width=device-width, initial-scale=1.0">`**: configura a área visível da página para responsividade em dispositivos móveis.
- **`<title>`**: define o título exibido na aba do navegador e nos resultados de busca.
- Links para folhas de estilo CSS (`<link rel="stylesheet" href="...">`) e fontes externas também ficam dentro de `<head>`.

### 4. `<body>`

- Contém todo o **conteúdo visível** da página: textos, imagens, vídeos, links, botões, seções estruturais e formulários.
