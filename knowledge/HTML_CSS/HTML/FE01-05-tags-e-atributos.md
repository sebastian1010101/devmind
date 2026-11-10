# FE01-05 — Tags e Atributos

## O que são Tags?

Tags são as instruções fundamentais do HTML. Elas são delimitadas pelos caracteres menor que (`<`) e maior que (`>`). A maioria das tags possui abertura e fechamento:

```html
<nome-da-tag>Conteúdo do elemento</nome-da-tag>
```

- **Tag de abertura:** `<p>`
- **Conteúdo:** o texto ou outros elementos aninhados
- **Tag de fechamento:** `</p>` (possui a barra inclinada `/`)
- **Elemento HTML:** o conjunto formado por abertura + conteúdo + fechamento

### Tags Autocontidas (Self-closing / Void Elements)

Alguns elementos não envolvem texto nem outros elementos. Por isso, não possuem tag de fechamento:

```html
<img src="foto.jpg" alt="Descrição da imagem">
<input type="text">
<br>
<hr>
```

---

## O que são Atributos?

Atributos fornecem propriedades adicionais e configurações aos elementos. Eles são declarados sempre na **tag de abertura**, geralmente no padrão `nome="valor"`.

```html
<a href="https://kenzie.com.br" target="_blank">Acessar Kenzie</a>
```

Neste exemplo:

- `href` é o atributo que define o destino do link.
- `target` define onde abrir o link (`_blank` abre em nova aba).

### Atributos Globais Comuns

Existem atributos válidos em praticamente todas as tags HTML:

| Atributo | Descrição | Exemplo |
| --- | --- | --- |
| `id` | Identificador único do elemento na página | `id="cabecalho-principal"` |
| `class` | Classe identificadora (pode ser compartilhada entre múltiplos elementos) | `class="card card-destaque"` |
| `style` | Aplica estilos CSS inline | `style="color: blue;"` |
| `title` | Texto complementar exibido como tooltip ao passar o mouse | `title="Clique para saber mais"` |
| `lang` | Define o idioma do conteúdo do elemento | `lang="pt-BR"` |

### Atributos Booleanos

Alguns atributos não precisam de valor atribuído; sua simples presença já ativa o comportamento:

```html
<!-- disabled impede a interação com o botão -->
<button disabled>Enviar</button>

<!-- required torna o campo obrigatório -->
<input type="email" required>
```
