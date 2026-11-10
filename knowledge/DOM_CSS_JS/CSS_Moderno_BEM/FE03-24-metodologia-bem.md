# FE03-24 — Metodologia BEM

## O que é a Metodologia BEM?

**BEM** significa **Block, Element, Modifier** (Bloco, Elemento, Modificador). É uma das convenções de nomenclatura de classes CSS mais populares da indústria, criada pela Yandex para resolver os maiores problemas em projetos front-end:

- Conflitos acidentais de nomes de classes em arquivos diferentes.
- Especificidade descontrolada e dependência excessiva de seletores aninhados profundos.
- Dificuldade de saber o papel de um elemento olhando apenas para a folha de estilos.

---

## Os Três Pilares do BEM

### 1. Bloco (Block)
Uma entidade visual autônoma, independente e que faça sentido completo por si só (ex: `header`, `menu`, `card`, `button`).

Nomeação: `.bloco` (palavras compostas usam hífen único, ex: `.card-produto`).

### 2. Elemento (Element)
Uma parte interna do bloco que não tem sentido fora dele. É delimitado por **dois underscores (`__`)**:

Nomeação: `.bloco__elemento` (ex: `.card-produto__titulo`, `.card-produto__preco`).

### 3. Modificador (Modifier)
Uma variação de aparência, estado ou comportamento de um bloco ou elemento. É delimitado por **dois hífens (`--`)**:

Nomeação: `.bloco--modificador` ou `.bloco__elemento--modificador` (ex: `.card-produto--destaque`, `.btn--primario`, `.btn--desabilitado`).

---

## Exemplo Visual Completo

```html
<!-- BLOCO: card -->
<article class="card card--destaque">
  <!-- ELEMENTO: card__imagem -->
  <img src="foto.jpg" class="card__imagem" alt="Foto">

  <!-- ELEMENTO: card__corpo -->
  <div class="card__corpo">
    <!-- ELEMENTO: card__titulo -->
    <h2 class="card__titulo">Curso de Front-End</h2>

    <!-- ELEMENTO + MODIFICADOR: btn btn--sucesso -->
    <button class="btn btn--sucesso">Matricular</button>
  </div>
</article>
```

```css
/* Classes puras e diretas com especificidade plana (0,0,1,0) */
.card { ... }
.card--destaque { border: 2px solid gold; }
.card__imagem { width: 100%; }
.card__corpo { padding: 16px; }
.card__titulo { font-size: 20px; }
```
