# FE01-43 — Flexbox Editor

## Ferramentas Visuais de Inspeção Flexbox no Navegador

Tanto o Google Chrome quanto o Mozilla Firefox possuem editores visuais nativos e ferramentas de desenvolvedor (*DevTools*) integradas para facilitar o entendimento e a prototipação de layouts Flexbox.

---

## Como Acessar o Flexbox Editor no DevTools

1. Abra qualquer página web no navegador.
2. Pressione a tecla `F12` (ou clique com o botão direito e selecione **Inspecionar**).
3. Na aba **Elementos (Elements)**, localize qualquer tag que possua a propriedade `display: flex`.
4. Você notará um pequeno selo/badge escrito **`flex`** ao lado do nome da tag.
5. Na aba lateral **Estilos (Styles)**, ao lado da linha `display: flex`, há um pequeno ícone de grade/painel. Ao clicar nele, abre-se o **Flexbox Editor visual**.

---

## Recursos Interativos do Flexbox Editor

O editor visual permite testar propriedades em tempo real com botões gráficos e ícones explicativos, sem precisar digitar código:

- **Direção (`flex-direction`):** ícones com setas indicando linha (`row`), coluna (`column`) ou invertidos.
- **Distribuição no Eixo Principal (`justify-content`):** botões visuais que mostram o espaçamento entre as caixas.
- **Alinhamento no Eixo Transversal (`align-items`):** opções de topo, centro, base ou esticar (`stretch`).
- **Quebra de Linha (`flex-wrap`):** ativa ou desativa o encapsulamento em múltiplas linhas.

---

## Visualização das Linhas de Grade e Eixos

Ao clicar no badge `flex` na árvore do DOM, o navegador desenha linhas pontilhadas coloridas sobre a tela exibindo:
- A área total do container.
- O traçado do eixo principal e transversal.
- As margens e os espaços livres que sobram no container flexível.
