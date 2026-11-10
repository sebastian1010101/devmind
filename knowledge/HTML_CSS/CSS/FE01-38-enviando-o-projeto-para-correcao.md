# FE01-38 — Enviando o Projeto para Correção

## Boas Práticas Antes da Entrega de Projetos

Na rotina da formação Kenzie Academy (e no desenvolvimento profissional em equipes de tecnologia), antes de submeter um projeto para revisão de código (*code review*) ou avaliação técnica, é fundamental realizar um checklist criterioso de garantia de qualidade.

---

## Checklist de Pré-Entrega

### 1. Validação de HTML e CSS
- O código HTML fecha todas as tags abertas corretamente?
- A estrutura possui a declaração `<!DOCTYPE html>`, `<html lang="pt-BR">` e metadados de charset e viewport?
- Todas as imagens possuem o atributo `alt` preenchido conscientemente?
- Não há regras de CSS inline perdidas dentro das tags HTML?

### 2. Organização e Limpeza de Arquivos
- Nomes de arquivos e pastas em minúsculas, sem espaços, acentos ou caracteres especiais (ex: `index.html`, `style.css`, pasta `img/`).
- O arquivo principal de entrada do projeto deve se chamar rigorosamente `index.html` na raiz do diretório.
- Remoção de códigos comentados que não têm mais uso e arquivos de rascunho temporários.

### 3. Indentação e Formatação de Código
- Todo o código deve estar identado com padrão consistente (2 espaços ou 4 espaços por nível).
- O atalho do VS Code `Shift + Alt + F` (ou `Format Document`) padroniza o documento instantaneamente.

### 4. Responsividade e Testes de Navegador
- A página foi testada no modo de inspeção do navegador (`F12` > ícone de dispositivos móveis)?
- Nenhum elemento transborda lateralmente gerando barra de rolagem horizontal indesejada?

---

## Fluxo Típico de Entrega via Git e GitHub

1. Inicializar o repositório ou verificar o status dos arquivos:
   ```bash
   git status
   ```
2. Adicionar as alterações realizadas:
   ```bash
   git add .
   ```
3. Criar uma mensagem de commit clara e descritiva:
   ```bash
   git commit -m "feat: implementa estrutura e estilizacao do blog"
   ```
4. Enviar para o repositório remoto no GitHub:
   ```bash
   git push origin main
   ```
5. Conferir se a página publicada no **GitHub Pages** (se aplicável) está acessível e com os links funcionando.
