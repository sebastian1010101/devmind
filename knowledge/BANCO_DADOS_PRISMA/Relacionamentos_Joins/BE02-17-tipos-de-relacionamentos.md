# BE02-17 — Tipos de Relacionamentos

## Por que relacionar

Dados normalizados vivem em tabelas separadas — **relacionamentos** são o que as conecta. A ligação é feita por chave estrangeira.

## Os três tipos

```text
1-1   um registro se liga a no máximo um outro
1-N   um registro se liga a vários outros
N-N   vários se ligam a vários
```

### Um para um (1-1)

```text
usuario ──── perfil
  1    tem    1
```

Cada usuário tem **no máximo um** perfil. Exemplos: pessoa↔passaporte, produto↔detalhes_técnicos, pedido↔nota_fiscal.

### Um para muitos (1-N)

```text
autor ────< livros
  1   escreve  N
```

Um autor escreve **muitos** livros; cada livro pertence a **um** autor. O mais comum de todos — pai/filhos, categoria/produtos, usuário/pedidos.

### Muitos para muitos (N-N)

```text
estudante >───< curso
    N   faz    N
```

Um estudante faz **muitos** cursos; um curso tem **muitos** estudantes. Não existe ligação direta — precisa de **tabela intermediária** (`matriculas`).

## Como identificar o tipo

Pergunte nos dois sentidos:

```text
"Um autor pode ter quantos livros?" → muitos
"Um livro pode ter quantos autores?" → um
=> 1-N

"Um estudante faz quantos cursos?" → muitos
"Um curso tem quantos estudantes?" → muitos
=> N-N
```

A resposta no formato `um/muitos` de cada lado define o tipo.

## Como implementar cada um

| Tipo | Onde fica a FK |
| --- | --- |
| 1-1 | Em qualquer lado — com `UNIQUE` na FK |
| 1-N | No lado **N** — o "muitos" aponta para o "um" |
| N-N | Tabela intermediária com 2 FKs |

```text
1-N:  livros.autor_id → autores.id
N-N:  matriculas.estudante_id → estudantes.id
      matriculas.curso_id     → cursos.id
```

## Decidindo na modelagem

- Dado que **pertence** a outro (telefone do usuário)? → 1-N ou tabela separada
- Dado que **detalha** outro 1:1 (configurações do usuário)? → 1-1
- Ligação que **gera dados próprios** (matrícula tem data, nota)? → N-N com tabela intermediária

## Resumo

- 1-1: um pra um — FK com `UNIQUE`
- 1-N: um pra muitos — FK no lado N (o mais comum)
- N-N: muitos pra muitos — tabela intermediária com 2 FKs
- Identifique perguntando "quantos?" nos dois sentidos da relação
