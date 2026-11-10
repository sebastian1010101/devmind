# BE02-41 — Prisma: Create com Relacionamento

## As três formas de ligar

```text
data.livros.create   → cria o filho junto (nested write)
data.livros.connect  → liga a um filho existente
data.autorId         → FK direta, quando já tem o id
```

## create aninhado — pai cria filho

```ts
const autor = await prisma.autor.create({
  data: {
    nome: "Machado de Assis",
    livros: {
      create: [
        { titulo: "Dom Casmurro" },
        { titulo: "Brás Cubas" },
      ],
    },
  },
  include: { livros: true },
});
```

Uma chamada, uma transação implícita — autor e livros criados juntos.

## Filho criando com pai — lado inverso

```ts
const livro = await prisma.livro.create({
  data: {
    titulo: "Quincas Borba",
    autor: {
      create: { nome: "Machado de Assis" },   // cria o pai junto
    },
  },
});
```

O Prisma resolve a ordem: cria o autor primeiro (precisa do id para a FK).

## connect — ligar a existente

```ts
await prisma.livro.create({
  data: {
    titulo: "Memórias Póstumas",
    autor: { connect: { id: 1 } },          // liga ao autor 1
  },
});

// por campo único também funciona
await prisma.livro.create({
  data: {
    titulo: "X",
    autor: { connect: { email: "machado@mail.com" } },
  },
});
```

## FK direta — o atalho

```ts
await prisma.livro.create({
  data: { titulo: "Esaú e Jacó", autorId: 1 },
});
```

Mesmo efeito que `connect: { id: 1 }` — mais curto quando você só tem o id.

## createOrConnect

```ts
await prisma.livro.create({
  data: {
    titulo: "Helena",
    autor: {
      connectOrCreate: {
        where: { email: "machado@mail.com" },
        create: { nome: "Machado", email: "machado@mail.com" },
      },
    },
  },
});
```

"Conecta se existir, cria se não" — útil em seeds e imports.

## N-N — connect em lista

```ts
await prisma.estudante.create({
  data: {
    nome: "Ana",
    cursos: { connect: [{ id: 1 }, { id: 2 }] },   // liga a 2 cursos
  },
});
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `P2025` no connect | O id ligado não existe — connect exige registro real |
| create aninhado falhou no meio | É transacional — ou cria tudo ou nada |
| `autor` vs `autorId` misturados | Escolha um: ou campo de relação ou FK direta — não os dois |
| connect em campo que não é unique | `connect` por campo exige `@unique` |
| Criar junção explícita via nested | Com junção explícita, crie o model dela (`prisma.matricula.create`) |

## Resumo

- `create` aninhado cria pai+filhos atomicamente
- `connect` liga a registro existente (por `@id` ou `@unique`)
- `autorId: 1` direto funciona e é mais simples quando você tem o id
- `connectOrCreate` = "conecta ou cria" — seeds e imports
