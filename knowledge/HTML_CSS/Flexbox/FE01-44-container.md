# FE01-44 — Container

## O Conceito de Container no Design de Interfaces

O **Container** (geralmente nomeado com a classe `.container`) é o elemento estrutural mais importante para manter a coerência visual de um site. Sua função é:

1. **Definir uma largura máxima centralizada:** evitar que o conteúdo se espalhe descontroladamente em monitores ultra-wide (4K, telas largas), o que tornaria a leitura cansativa.
2. **Garantir margens de respiro laterais:** impedir que o conteúdo fique colado nas bordas do visor em telas de celular.

---

## O Padrão Universal de Container

```css
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 16px;
  padding-right: 16px;
}
```

- `width: 100%`: garante fluidez total em dispositivos menores.
- `max-width: 1200px`: impõe um limite estético harmonioso em computadores.
- `margin: 0 auto`: a técnica universal de centralização horizontal para elementos de bloco.
- `padding: 0 16px`: a margem de segurança para telas pequenas.

---

## Combinando Container e Flexbox

O erro comum de iniciantes é aplicar `display: flex` diretamente no mesmo elemento do container centralizador, o que pode misturar responsabilidades.

A arquitetura recomendada separa a seção da área de conteúdo:

```html
<!-- A SECTION cuida da cor de fundo de ponta a ponta na tela -->
<section class="secao-beneficios">
  <!-- O CONTAINER cuida da largura máxima e centralização -->
  <div class="container container-flex">
    <div class="item">Benefício 1</div>
    <div class="item">Benefício 2</div>
    <div class="item">Benefício 3</div>
  </div>
</section>
```

```css
.secao-beneficios {
  background-color: #f1f5f9; /* Fundo ocupa 100% da largura da janela */
  padding: 64px 0;
}

.container-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}
```
