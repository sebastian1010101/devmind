# FE04-01 — Notion: Montando seu Acervo de Conhecimento

## Por que um acervo de conhecimento

Desenvolvimento é aprendizado contínuo — você encontrará os mesmos problemas, padrões e soluções repetidamente. Sem um sistema para registrar, cada descoberta vira uma pesquisa nova. Com um **acervo de conhecimento**, cada solução fica a um clique de distância.

## O que é o Notion

Notion é um workspace all-in-one: blocos de texto, listas, tabelas, bancos de dados, wikis — tudo numa interface flexível que combina documento e organização. Para devs, funciona como um "segundo cérebro" técnico.

## Estrutura recomendada

### A base: Snippets e Soluções

A peça mais valiosa — um banco de dados com problemas resolvidos:

```text
Banco de dados: "Meu Acervo"
├── Título       → descrição curta do problema/solução
├── Tags         → react, css, git, debugging, api
├── Linguagem    → javascript, css, html, sql
├── Dificuldade  → fácil, médio, difícil
├── Fonte        → link da documentação ou Stack Overflow
└── Conteúdo     → o código/explicação em si
```

### Organização por módulo do curso

```text
📁 Kenzie — Front-End
├── 📁 Módulo 1 — HTML/CSS
│   ├── 📄 Flexbox — cheat sheet
│   ├── 📄 Seletores CSS avançados
│   └── 📄 Box Model e especificidade
├── 📁 Módulo 2 — JavaScript
│   ├── 📄 Métodos de array
│   ├── 📄 Async/await
│   └── 📄 Destructuring patterns
├── 📁 Módulo 3 — DOM
│   └── 📄 Event delegation
└── 📁 Módulo 4 — React
    ├── 📄 Hooks — useState
    ├── 📄 Hooks — useEffect
    └── 📄 Props e children patterns
```

## O que registrar

### Patterns que você usa sempre

```text
Exemplo de entrada:
Título: "Fetch com loading e erro"
Tags: react, useEffect, fetch
Snippet:
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);
  // ...
```

### Erros que você já resolveu

```text
Título: "CORS error ao chamar API"
Problema: "Access to fetch blocked by CORS policy"
Solução: Verificar se a API aceita a origem; usar proxy em dev
Tags: api, cors, debug
```

### Comandos que você sempre esquece

```text
Título: "Git — desfazer último commit mantendo mudanças"
Comando: git reset --soft HEAD~1
Tags: git, comandos
```

## Boas práticas do acervo

### 1. Registre no momento da solução

Não deixe para depois — quando resolve um problema difícil, gaste 2 minutos registrando. A memória fresca escreve a melhor documentação.

### 2. Escreva para você do futuro

```text
❌ "arrumei o css"
✅ "CSS — o overflow do card estava vazando porque o pai não tinha overflow:hidden"
```

Você daqui a 6 meses não lembra do contexto — inclua o *porquê*, não só o *o quê*.

### 3. Tags consistentes

Escolha um vocabulário fixo e mantenha — `react`, `css`, `debugging`, `api`, `sql`. Tags inventadas na hora viram ruído.

### 4. Links são ouro

Registre a fonte — documentação oficial, artigo, discussão do Stack Overflow. O snippet resolve o imediato; o link explica o porquê.

### 5. Revise e atualize

O acervo não é estático — quando descobrir uma forma melhor, atualize a entrada. Um acervo desatualizado é pior que nenhum.

## Alternativas ao Notion

| Ferramenta | Vantagem |
| --- | --- |
| **Obsidian** | Markdown local, grafo de links entre notas |
| **Notion** | Visual, databases flexíveis, templates |
| **GitHub Gists** | Snippets versionados, compartilháveis |
| **README no projeto** | Notas no contexto do código |
| **Pasta de .md** | Simples — literalmente o que este knowledge/ faz |

## A relação com o aprendizado

Registrar não é só organização — é **revisão ativa**. O ato de escrever a solução com suas próprias palavras consolida o aprendizado. Quem documenta aprende duas vezes: uma resolvendo, outra explicando.

## Começando hoje

1. Crie uma página "Acervo" no Notion
2. Adicione um banco de dados com colunas: Título, Tags, Linguagem, Conteúdo
3. Registre as 3 últimas coisas que você pesquisou
4. Comece o hábito: problema resolvido → 2 minutos no acervo
