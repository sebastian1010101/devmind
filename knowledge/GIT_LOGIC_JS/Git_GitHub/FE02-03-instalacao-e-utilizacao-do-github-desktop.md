# FE02-03 — Instalação e Utilização do GitHub Desktop

## O que é o GitHub Desktop?

O **GitHub Desktop** é o aplicativo oficial com interface gráfica (GUI) desenvolvido pela equipe do GitHub. Ele permite que desenvolvedores executem os fluxos de trabalho comuns do Git sem precisar memorizar comandos de terminal.

---

## Principais Recursos Visuais

- **Visualização de Diferenças (Diff):** exibe linhas adicionadas (em verde com sinal `+`) e linhas removidas (em vermelho com sinal `-`) de maneira clara antes de criar o commit.
- **Gerenciamento de Branches:** criação, troca e fusão (*merge*) de branches com apenas um clique.
- **Histórico Gráfico:** linha do tempo visual de todos os commits realizados no projeto com autores e mensagens.
- **Sincronização Simples:** botão único para buscar alterações remotas (*Fetch*), baixar novidades (*Pull*) e enviar commits locais (*Push*).

---

## Fluxo de Trabalho Passo a Passo no GitHub Desktop

### 1. Clonando ou Criando um Repositório

- **Clonar:** menu `File > Clone Repository...`, selecione um projeto existente na sua conta do GitHub e escolha a pasta local de destino.
- **Criar novo:** menu `File > New Repository...`, informe o nome, descrição, marque inicialização com README e clique em *Create Repository*.

### 2. Criando um Commit Visualmente

1. Edite os arquivos normalmente no VS Code e salve.
2. Ao voltar para o GitHub Desktop, note a lista de arquivos alterados listada na coluna lateral esquerda (*Changes*).
3. Na parte inferior esquerda, preencha:
   - **Summary (Obrigatório):** título conciso do que foi alterado.
   - **Description (Opcional):** detalhes adicionais da motivação da alteração.
4. Clique no botão azul **Commit to main**.

### 3. Enviando para o GitHub (Push)

- Clique no botão **Publish branch** (na primeira vez) ou **Push origin** no topo da janela para enviar seus commits locais aos servidores do GitHub.

---

## Terminal vs Interface Gráfica

Embora o GitHub Desktop seja uma excelente ferramenta para visualizar alterações complexas, dominar os comandos fundamentais do terminal (`git add`, `git commit`, `git push`, `git status`) é crucial para a carreira de desenvolvedor, pois servidores de produção, pipelines de CI/CD e ambientes em nuvem não possuem interface gráfica.
