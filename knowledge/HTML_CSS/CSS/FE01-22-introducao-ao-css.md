# FE01-22 — Introdução ao CSS

## O que é CSS?

**CSS** significa *Cascading Style Sheets* (Folhas de Estilo em Cascata). É a linguagem padrão utilizada para descrever a **apresentação visual e o layout** de documentos estruturados em HTML.

Enquanto o HTML define o que cada elemento é (título, parágrafo, botão), o CSS determina como esses elementos serão exibidos visualmente: cores, fontes, espaçamentos, tamanhos, bordas e alinhamentos em diferentes telas.

---

## O Conceito de Cascata e Herança

O nome "Folhas de Estilo em Cascata" vem de dois princípios centrais:

1. **Cascata:** quando múltiplas regras de estilo entram em conflito sobre o mesmo elemento, o navegador resolve o conflito combinando três critérios:
   - **Origem:** estilos do autor do site têm prioridade sobre os estilos padrão do navegador.
   - **Especificidade:** regras com seletores mais precisos sobrepõem regras genéricas.
   - **Ordem de declaração:** caso a especificidade seja igual, a última regra declarada no código prevalece.

2. **Herança:** propriedades aplicadas a um elemento pai (como `color` e `font-family`) são transmitidas automaticamente aos seus elementos filhos, a menos que sejam explicitamente sobrescritas.

---

## Vantagens da Separação entre Conteúdo e Apresentação

- **Manutenibilidade:** alterar o design completo de um portal com centenas de páginas editando apenas um arquivo `.css`.
- **Reaproveitamento:** as mesmas classes visuais podem ser utilizadas em múltiplos componentes.
- **Performance:** o navegador faz cache do arquivo de estilo externo após a primeira requisição.
- **Acessibilidade:** permite que leitores de tela processem o conteúdo puro em HTML sem interferência de regras visuais.
