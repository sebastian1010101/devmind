# FE02-00 — Introdução ao Git e GitHub

## O que é Controle de Versão?

Um **Sistema de Controle de Versão** (VCS - *Version Control System*) é uma ferramenta projetada para registrar o histórico de alterações feitas em arquivos ao longo do tempo. Ele permite:

- Recuperar versões anteriores de qualquer arquivo caso ocorra um erro ou bug.
- Visualizar exatamente quem fez cada modificação, quando e por qual motivo.
- Trabalhar em equipe simultaneamente no mesmo projeto sem sobrescrever o trabalho de outros colegas.

---

## A Diferença Fundamental entre Git e GitHub

Uma confusão muito comum entre iniciantes é acreditar que Git e GitHub são a mesma coisa:

| Característica | Git | GitHub |
| --- | --- | --- |
| **O que é?** | Software de controle de versão distribuído | Plataforma e serviço em nuvem |
| **Onde roda?** | Localmente na máquina do desenvolvedor (offline) | Remotamente em servidores web da Microsoft |
| **Interface** | Linha de comando no terminal (CLI) ou clientes locais | Interface web gráfica no navegador |
| **Finalidade Principal** | Criar commits, controlar branches e histórico | Hospedar repositórios remotos, colaborar em equipe e pull requests |

---

## Os Três Estados do Git Local

Para compreender o Git, é essencial dominar suas três áreas fundamentais:

```text
+---------------------+     git add     +---------------------+    git commit   +---------------------+
|                     | --------------> |                     | --------------> |                     |
|   WORKING TREE      |                 |    STAGING AREA     |                 |    LOCAL REPO       |
|  (Arquivos em       |                 |  (Área de Preparação|                 |  (Histórico salvo   |
|   modificação)      | <-------------- |   para o commit)    |                 |   no banco .git)    |
|                     |  git restore    |                     |                 |                     |
+---------------------+                 +---------------------+                 +---------------------+
```

1. **Working Tree (Diretório de Trabalho):** a pasta onde você edita arquivos de código no VS Code.
2. **Staging Area / Index:** a área de preparação onde você seleciona quais alterações específicas farão parte do próximo registro oficial.
3. **Local Repository (Repositório Local):** o banco de dados interno na pasta oculta `.git` onde o histórico permanente de commits fica armazenado com segurança na sua máquina.
