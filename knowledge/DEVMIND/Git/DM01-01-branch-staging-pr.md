# DM01-01 — Branches, staging e pull requests

## Tirar um arquivo do staging

Imagine que você editou `README.md` e o adicionou com `git add README.md`. Se quiser que a próxima confirmação deixe esse arquivo de fora, use `git restore --staged README.md`. A opção altera o índice (staging area) e preserva o conteúdo que você está editando. Use `git diff --staged` para conferir o próximo commit e `git diff` para conferir o que está fora dele.

## Da branch à revisão no GitHub

Crie uma branch com `git switch -c docs/guia`, faça o commit e envie a branch com `git push -u origin docs/guia`. Um pull request no GitHub propõe integrar a branch de origem à branch de destino. A equipe pode comentar o diff, pedir ajustes e acompanhar as verificações antes da integração.

Referências [git restore](https://git-scm.com/docs/git-restore) e [GitHub Pull Requests](https://docs.github.com/en/pull-requests/reference/pull-requests).
