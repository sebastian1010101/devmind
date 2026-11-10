# FE01-04 — Introdução ao HTML

## O que é HTML?

**HTML** significa *HyperText Markup Language* (Linguagem de Marcação de Hipertexto). Não é uma linguagem de programação (não possui lógica, variáveis de execução ou laços de repetição), mas sim uma **linguagem de marcação** utilizada para estruturar e dar significado ao conteúdo exibido em navegadores web.

- **Hipertexto (HyperText):** refere-se a textos interconectados por meio de links (*hiperlinks*), permitindo navegar entre páginas e recursos.
- **Marcação (Markup):** define o uso de marcas (*tags*) que indicam ao navegador o papel de cada parte do conteúdo (título, parágrafo, botão, tabela, imagem, etc.).

---

## Papel na Tríade da Web

Na construção de aplicações web, três tecnologias fundamentais atuam em conjunto:

| Tecnologia | Função Principal | Analogia |
| --- | --- | --- |
| **HTML** | Estrutura e Conteúdo | O esqueleto e as paredes de uma casa |
| **CSS** | Apresentação e Estilo | A pintura, decoração e layout da casa |
| **JavaScript** | Comportamento e Interatividade | A fiação elétrica, interruptores e automação |

---

## Como o Navegador Interpreta o HTML

1. O navegador faz uma requisição HTTP a um servidor web ou lê um arquivo local (`.html`).
2. O motor do navegador realiza o processamento (*parsing*) do texto HTML.
3. Cria a árvore de objetos em memória chamada **DOM** (*Document Object Model*).
4. Aplica os estilos CSS sobre o DOM e renderiza a página final na tela.

---

## Resumo dos Pontos-Chave

- Todo arquivo HTML possui extensão `.html` (por exemplo, `index.html`).
- A versão padrão atual é o **HTML5**.
- O HTML fornece a semântica necessária para que mecanismos de busca (SEO) e tecnologias assistivas (leitores de tela para acessibilidade) entendam o documento.
