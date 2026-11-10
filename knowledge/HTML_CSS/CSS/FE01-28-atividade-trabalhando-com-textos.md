# FE01-28 — Atividade: Trabalhando com Textos

## Objetivo da Atividade

Aprimorar a apresentação visual de uma página de leitura (artigo ou crônica), praticando propriedades tipográficas: hierarquia de tamanhos, pesos, alinhamentos, espaçamentos entre linhas e remoção de decorações padrão de links.

---

## Enunciado do Desafio

Crie uma folha de estilos `artigo.css` para estilizar a publicação de uma matéria de tecnologia, atendendo aos seguintes critérios:

1. Configuração global no `body`:
   - Família tipográfica: `system-ui, -apple-system, sans-serif`.
   - Tamanho base de 16px e cor de texto grafite suave (`#2d3748`).
   - Espaçamento de linha relaxado (`line-height: 1.7`).
2. Título principal (`h1`):
   - Tamanho `36px`, peso `700` (negrito), cor `#1a202c`.
   - Alinhamento centralizado.
3. Subtítulo descritivo (`.subtitulo`):
   - Tamanho `18px`, cor cinza média (`#718096`), alinhamento centralizado.
   - Espaço inferior para afastar do corpo do artigo.
4. Cabeçalho de seção (`h2`):
   - Tamanho `24px`, cor `#2b6cb0`, borda inferior decorativa de 2px sólida.
5. Parágrafos (`p`):
   - Alinhamento justificado ou à esquerda com recuo de margem inferior de 16px.
6. Links dentro do texto (`p a`):
   - Cor azul de destaque (`#3182ce`), sem sublinhado inicial (`text-decoration: none`).
   - Sublinhado ativado ao passar o mouse (`:hover`).

---

## Solução de Referência

```css
body {
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 16px;
  color: #2d3748;
  line-height: 1.7;
  max-width: 720px;
  margin: 0 auto;
  padding: 32px 16px;
}

h1 {
  font-size: 36px;
  font-weight: 700;
  color: #1a202c;
  text-align: center;
  margin-bottom: 8px;
}

.subtitulo {
  font-size: 18px;
  color: #718096;
  text-align: center;
  margin-bottom: 32px;
}

h2 {
  font-size: 24px;
  color: #2b6cb0;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 6px;
  margin-top: 28px;
  margin-bottom: 16px;
}

p {
  margin-bottom: 16px;
}

p a {
  color: #3182ce;
  text-decoration: none;
  font-weight: 600;
}

p a:hover {
  text-decoration: underline;
}
```
