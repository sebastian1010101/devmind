# FE01-12 — Hyperlinks

## A Tag de Link (`<a>`)

A tag `<a>` (*anchor*) é o elemento que transforma a web em uma rede de hipertexto, permitindo navegar entre documentos, baixar arquivos ou saltar para seções internas.

O atributo mais importante é o `href` (*Hypertext Reference*), que aponta para o endereço de destino.

```html
<a href="https://kenzie.com.br">Visitar Kenzie</a>
```

---

## Tipos de Caminhos e Destinos

### 1. Links Externos (URLs Absolutas)
Apontam para outros domínios na internet, incluindo o protocolo completo:

```html
<a href="https://developer.mozilla.org/pt-BR/" target="_blank" rel="noopener noreferrer">MDN Web Docs</a>
```

- `target="_blank"`: abre o link em uma nova aba do navegador.
- `rel="noopener noreferrer"`: boa prática de segurança para evitar vulnerabilidades de acesso à janela de origem (*window.opener*).

### 2. Links Internos (Caminhos Relativos)
Apontam para outras páginas dentro do mesmo projeto:

```html
<!-- Página na mesma pasta -->
<a href="sobre.html">Sobre Nós</a>

<!-- Página em subpasta -->
<a href="paginas/contato.html">Fale Conosco</a>

<!-- Voltar um nível de pasta -->
<a href="../index.html">Voltar para o Início</a>
```

### 3. Links Âncora (Navegação na Mesma Página)
Permitem pular diretamente para um elemento que possua um atributo `id` correspondente:

```html
<!-- Link que dispara a navegação -->
<a href="#contato">Ir para a seção de contato</a>

<!-- Mais abaixo na mesma página -->
<section id="contato">
  <h2>Entre em Contato</h2>
</section>
```

### 4. Protocolos Especiais (Email e Telefone)

```html
<a href="mailto:contato@empresa.com">Enviar E-mail</a>
<a href="tel:+5511999999999">Ligar para Suporte</a>
```
