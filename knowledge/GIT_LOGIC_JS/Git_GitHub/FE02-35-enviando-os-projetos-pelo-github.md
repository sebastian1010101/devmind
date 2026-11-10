# FE02-35 — Enviando os Projetos pelo GitHub

## O Ciclo Completo de Envio de Projetos via Linha de Comando

A entrega de atividades e projetos práticos na Kenzie Academy (e no mercado de trabalho em geral) segue um fluxo rigoroso de controle de versão. Dominar esses comandos no terminal garante independência e segurança no gerenciamento de código.

---

## 1. Inicializando um Projeto Local

Caso esteja começando uma pasta nova a partir do zero na sua máquina:

```bash
# 1. Entrar na pasta do projeto
cd meu-projeto

# 2. Inicializar o repositório Git local
git init

# 3. Conferir o estado atual dos arquivos
git status
```

---

## 2. O Ciclo Diário: Modificar, Preparar e Commitar

Sempre que concluir uma funcionalidade, corrigir um bug ou finalizar uma seção:

```bash
# 1. Verificar arquivos criados ou modificados
git status

# 2. Adicionar os arquivos alterados para a Staging Area
git add .
# (Ou adicionar arquivos específicos: git add index.html style.css)

# 3. Registrar o commit com uma mensagem descritiva e clara
git commit -m "feat: cria estrutura e estilizacao inicial do projeto"
```

---

## 3. Conectando com o Repositório Remoto no GitHub

1. Crie um repositório vazio no GitHub (sem marcar inicialização com README ou .gitignore).
2. Copie a URL do repositório (preferencialmente a URL SSH se você já configurou suas chaves):

```bash
# 1. Vincular o repositório local ao remoto (apelidado tradicionalmente de 'origin')
git remote add origin git@github.com:seu-usuario/nome-do-projeto.git

# 2. Garantir que a branch principal se chame 'main'
git branch -M main

# 3. Enviar os commits pela primeira vez (com flag -u para vincular o rastreamento)
git push -u origin main
```

---

## 4. Envios Posteriores Durante o Desenvolvimento

Nos envios seguintes do mesmo projeto, você precisa apenas de:

```bash
git add .
git commit -m "fix: ajusta alinhamento dos cards responsivos"
git push
```

---

## 5. Boas Práticas para Mensagens de Commit

Mensagens de commit devem expressar claramente **o que** foi feito e **por que**, utilizando convenções consagradas pela comunidade (como *Conventional Commits*):

- `feat:` para uma nova funcionalidade (ex: `feat: adiciona secao de depoimentos`).
- `fix:` para correção de bugs ou falhas (ex: `fix: corrige quebra de linha no menu mobile`).
- `style:` para formatações visuais, espaços e estilos que não afetam a lógica.
- `refactor:` para refatorações e melhorias de código sem alterar o comportamento externo.
- `docs:` para alterações em documentações e arquivos README.
