# FE01-10 — Atividade: Estruturando um Documento HTML

## Objetivo da Atividade

Praticar a criação do primeiro documento HTML completo a partir do zero, aplicando a estrutura básica do HTML5, metadados essenciais e tags fundamentais de texto.

---

## Enunciado do Desafio

Crie um arquivo chamado `index.html` com os seguintes requisitos:

1. Declaração do `DOCTYPE` correta para HTML5.
2. Tag `html` com definição do idioma em português do Brasil (`pt-BR`).
3. Cabeçalho (`head`) contendo:
   - Configuração de codificação UTF-8.
   - Configuração da viewport para dispositivos móveis.
   - Título da página: `"Meu Perfil Profissional"`.
4. Corpo da página (`body`) estruturado com:
   - Um título principal (`h1`) com o seu nome.
   - Um subtítulo (`h2`) com a profissão ou objetivo (ex: `"Desenvolvedor Web Full Stack"`).
   - Um parágrafo (`p`) descrevendo brevemente quem você é, utilizando tags `<strong>` para destacar suas principais habilidades.
   - Uma linha horizontal (`hr`) separando as seções.
   - Um subtítulo (`h2`) intitulado `"Sobre Meus Estudos"`.
   - Um parágrafo com as tecnologias que você está aprendendo atualmente.

---

## Solução de Referência

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Perfil Profissional</title>
  </head>
  <body>
    <h1>João Silva</h1>
    <h2>Desenvolvedor Web Front-End em Formação</h2>
    <p>
      Olá! Sou estudante de tecnologia apaixonado por criar interfaces web acessíveis e eficientes. Minhas principais competências incluem <strong>HTML5</strong>, <strong>CSS3</strong> e lógica de programação.
    </p>

    <hr>

    <h2>Sobre Meus Estudos</h2>
    <p>
      Atualmente dedico meus estudos aos fundamentos da web na <em>Kenzie Academy</em>, aprendendo a estruturar páginas com semântica adequada e boas práticas de código.
    </p>
  </body>
</html>
```
