# FE01-26 — Atividade: Seletores e Cores

## Objetivo da Atividade

Praticar a criação de folhas de estilo externas, aplicando regras com seletores de tipo, classe e id, além de experimentar diferentes formatos de cor (Hexadecimal e RGB/RGBA).

---

## Enunciado do Desafio

Dado o arquivo HTML de um cartão de apresentação pessoal, crie um arquivo `style.css` vinculado externamente que atenda aos seguintes requisitos visuais:

1. Fundo do documento (`body`) com uma cor cinza clara neutra (`#f4f6f8`).
2. O container principal com a classe `.perfil-card` deve ter:
   - Fundo totalmente branco (`#ffffff`).
   - Borda sutil de 1px sólida na cor cinza média (`#d0d7de`).
   - Borda arredondada suave.
3. O nome principal com o id `#nome-dev` deve ter a cor `#0969da`.
4. O cargo com a classe `.cargo` deve ter a cor cinza escura `#57606a`.
5. Um botão de contato com a classe `.btn-contato`:
   - Fundo verde institucional usando código hexadecimal (`#2da44e`).
   - Cor do texto em branco.
6. Uma caixa de aviso secundária com a classe `.status-badge` utilizando fundo semi-transparente via `rgba` (`rgba(45, 164, 78, 0.15)`) e cor verde escura.

---

## Solução de Referência

### Estrutura HTML (`index.html`)

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cartão de Perfil</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <main class="perfil-card">
      <h1 id="nome-dev">Sebastián Silva</h1>
      <p class="cargo">Desenvolvedor Front-End Júnior</p>
      <span class="status-badge">Disponível para Projetos</span>
      <br><br>
      <button class="btn-contato">Entrar em Contato</button>
    </main>
  </body>
</html>
```

### Folha de Estilos (`style.css`)

```css
body {
  background-color: #f4f6f8;
  font-family: Arial, sans-serif;
  padding: 40px;
}

.perfil-card {
  background-color: #ffffff;
  border: 1px solid #d0d7de;
  border-radius: 8px;
  padding: 24px;
  max-width: 360px;
}

#nome-dev {
  color: #0969da;
  margin-bottom: 4px;
}

.cargo {
  color: #57606a;
  font-size: 14px;
}

.status-badge {
  background-color: rgba(45, 164, 78, 0.15);
  color: #1a7f37;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.btn-contato {
  background-color: #2da44e;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  cursor: pointer;
}
```
