# FE01-07 — Marcando Texto no HTML

## Hierarquia de Cabeçalhos (Headings)

O HTML fornece seis níveis de títulos, de `<h1>` até `<h6>`, ordenados por relevância e peso semântico:

```html
<h1>Título Principal da Página (apenas um recomendado por página)</h1>
<h2>Subtítulo de Seção Principal</h2>
<h3>Subseção do Título H2</h3>
<h4>Tópico Específico</h4>
<h5>Subtópico</h5>
<h6>Menor Nível de Título</h6>
```

> **Atenção Semântica:** Não utilize títulos apenas para mudar o tamanho visual da fonte (isso é papel do CSS). Respeite a hierarquia lógica do documento sem pular níveis (ex: não passe de `h1` direto para `h3`).

---

## Parágrafos e Quebras de Linha

- **`<p>`**: define um bloco de parágrafo com margens automáticas antes e depois.
- **`<br>`**: quebra de linha forçada (*line break*). Use apenas quando a quebra for parte do conteúdo (ex: endereços ou poesias).
- **`<hr>`**: quebra temática (*horizontal rule*), desenha uma linha separadora visual.

```html
<p>
  Primeira linha do parágrafo.<br>
  Segunda linha dentro do mesmo parágrafo.
</p>
<hr>
<p>Início de um novo assunto após a divisória.</p>
```

---

## Ênfase e Formatação Semântica de Texto

| Tag | Finalidade Semântica | Exibição Típica |
| --- | --- | --- |
| `<strong>` | Importância forte, seriedade ou urgência | Negrito |
| `<em>` | Ênfase com alteração de entonação | Itálico |
| `<b>` | Destaque estilístico sem importância especial | Negrito |
| `<i>` | Termo alternativo, estrangeirismo, pensamento | Itálico |
| `<mark>` | Texto destacado / marca-texto | Fundo amarelo |
| `<small>` | Informações secundárias, notas de rodapé, copyright | Fonte reduzida |
| `<del>` | Texto removido ou riscado | Linha sobre o texto |
| `<ins>` | Texto inserido ou adicionado | Sublinhado |
| `<sub>` | Texto subscrito (exemplo: fórmula da água H2O com índice rebaixado) | Linha inferior |
| `<sup>` | Texto sobrescrito (exemplo: expoentes como E = mc2) | Linha superior |
| `<code>` | Fragmentos curtos de código de programação | Fonte monoespaçada |
