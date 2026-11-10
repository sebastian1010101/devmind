# FE01-21 — Atividade: Criando Formulário de Cadastro

## Objetivo da Atividade

Integrar todos os elementos fundamentais de formulários HTML estudados na seção: campos de texto, e-mail, senha, rádio, select, textarea, agrupamento semântico com fieldset e botões de ação.

---

## Enunciado do Desafio

Crie um arquivo chamado `cadastro.html` contendo um formulário completo de cadastro de novos alunos para uma plataforma de cursos, cumprindo os critérios:

1. Tag `<form>` utilizando o método `POST` e direcionando para `/api/cadastro`.
2. **Seção 1 — Dados Pessoais** (agrupados por `<fieldset>` e `<legend>`):
   - Campo para **Nome Completo** (tipo texto, obrigatório, mínimo 3 caracteres).
   - Campo para **E-mail** (tipo e-mail, obrigatório).
   - Campo para **Senha** (tipo senha, obrigatório, mínimo 8 caracteres).
   - Campo para **Data de Nascimento** (tipo data).
3. **Seção 2 — Perfil do Aluno** (agrupados por `<fieldset>` e `<legend>`):
   - Seleção de **Nível de Experiência** usando botões de rádio com o mesmo `name`: *Iniciante*, *Intermediário*, *Avançado*. O *Iniciante* deve vir marcado por padrão (`checked`).
   - Seleção de **Curso de Interesse** usando menu suspenso `<select>` com opção inicial desabilitada e opções divididas por `<optgroup>` (*Front-End* e *Back-End*).
   - Campo `<textarea>` para **Biografia / Apresentação Pessoal** (com placeholder e altura de 4 linhas).
4. **Termos e Submissão:**
   - Caixa de seleção (`checkbox`) para aceitar os termos de uso (obrigatório).
   - Botão para limpar o formulário (`type="reset"`).
   - Botão principal de submissão do formulário (`type="submit"`).

---

## Solução de Referência

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro de Aluno - Kenzie Academy</title>
  </head>
  <body>
    <main>
      <h1>Formulário de Inscrição</h1>
      <p>Preencha os campos abaixo para iniciar seus estudos na área de tecnologia.</p>

      <form action="/api/cadastro" method="POST">
        <!-- Seção de Dados Pessoais -->
        <fieldset>
          <legend>Dados Pessoais</legend>

          <div>
            <label for="nome">Nome Completo:</label>
            <input type="text" id="nome" name="nome" placeholder="Ex: Maria Oliveira" minlength="3" required>
          </div>

          <div>
            <label for="email">E-mail:</label>
            <input type="email" id="email" name="email" placeholder="seuemail@exemplo.com" required>
          </div>

          <div>
            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" minlength="8" placeholder="Mínimo de 8 caracteres" required>
          </div>

          <div>
            <label for="data-nascimento">Data de Nascimento:</label>
            <input type="date" id="data-nascimento" name="data_nascimento">
          </div>
        </fieldset>

        <!-- Seção de Perfil -->
        <fieldset>
          <legend>Perfil e Interesses</legend>

          <div>
            <p>Qual o seu nível atual de conhecimento?</p>
            <input type="radio" id="iniciante" name="nivel" value="iniciante" checked>
            <label for="iniciante">Iniciante (começando do zero)</label>

            <input type="radio" id="intermediario" name="nivel" value="intermediario">
            <label for="intermediario">Intermediário</label>

            <input type="radio" id="avancado" name="nivel" value="avancado">
            <label for="avancado">Avançado</label>
          </div>

          <div>
            <label for="curso">Escolha a Formação:</label>
            <select id="curso" name="curso" required>
              <option value="" disabled selected>-- Selecione um curso --</option>
              <optgroup label="Front-End">
                <option value="html-css">Fundamentos HTML e CSS</option>
                <option value="react">Desenvolvimento com React</option>
              </optgroup>
              <optgroup label="Back-End">
                <option value="node">Node.js e Express</option>
                <option value="python">Python e Django</option>
              </optgroup>
            </select>
          </div>

          <div>
            <label for="bio">Sobre Você:</label><br>
            <textarea id="bio" name="bio" rows="4" cols="45" placeholder="Conte brevemente sobre seus objetivos e motivações..."></textarea>
          </div>
        </fieldset>

        <!-- Confirmação e Ações -->
        <div>
          <input type="checkbox" id="termos" name="termos" required>
          <label for="termos">Declaro que li e concordo com os Termos de Uso e Política de Privacidade.</label>
        </div>

        <div>
          <button type="reset">Limpar Campos</button>
          <button type="submit">Finalizar Inscrição</button>
        </div>
      </form>
    </main>
  </body>
</html>
```
