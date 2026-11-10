# BE02-53 — Atividade: Excluindo Dados

## Objetivo

Implementar exclusão correta nos services — 404 quando não existe, FK respeitada, e decisão entre hard e soft delete.

## Services de delete

```ts
// delete simples com 404 semântico
export async function deletarCurso(id: number) {
  const curso = await prisma.curso.findUnique({ where: { id } });
  if (!curso) throw new AppError("Curso não encontrado", 404);

  await prisma.curso.delete({ where: { id } });
}

// rota
router.delete("/cursos/:id", async (req, res) => {
  await deletarCurso(Number(req.params.id));
  return res.status(204).send();
});
```

## Delete com filhos — ordem importa

```ts
export async function deletarEstudante(id: number) {
  const estudante = await prisma.estudante.findUnique({ where: { id } });
  if (!estudante) throw new AppError("Estudante não encontrado", 404);

  // filhos primeiro, pai por último — atomicamente
  await prisma.$transaction([
    prisma.matricula.deleteMany({ where: { estudanteId: id } }),
    prisma.estudante.delete({ where: { id } }),
  ]);
}
```

Se a junção fosse `onDelete: Cascade` no schema, bastaria o `delete` direto — a escolha acontece na modelagem.

## Soft delete — implementando

```prisma
model Estudante {
  // ...
  deletadoEm DateTime? @map("deletado_em")
}
```

```ts
// "excluir" = marcar
export async function desativarEstudante(id: number) {
  return prisma.estudante.update({
    where: { id },
    data: { deletadoEm: new Date() },
  });
}

// todas as leituras filtram os mortos
export async function listarEstudantes() {
  return prisma.estudante.findMany({
    where: { deletadoEm: null },
  });
}

// "restaurar" = desmarcar
export async function restaurarEstudante(id: number) {
  return prisma.estudante.update({
    where: { id },
    data: { deletadoEm: null },
  });
}
```

## Os trade-offs

| Hard delete | Soft delete |
| --- | --- |
| Dado some — libera espaço | Dado fica — histórico e auditoria |
| FK bloqueia ou cascateia | Sem problema de FK |
| Queries simples | Toda query filtra `deletadoEm: null` |
| Irreversível | Recuperável |

## Testes de validação

```ts
// 404
await deletarCurso(999);   // deve lançar AppError 404

// integridade — não deixa órfãos
await deletarEstudante(1);
// matriculas do estudante 1 sumiram junto (transação ou cascade)

// soft delete
await desativarEstudante(2);
// listarEstudantes() não traz o id 2; restaurarEstudante(2) traz de volta
```

## Critérios de conclusão

1. DELETE retorna 204; id inexistente retorna 404
1. Estudante deletado sem deixar matrículas órfãs
1. Soft delete funciona como flag recuperável
1. Decisão hard vs soft documentada por entidade

## Resumo

- `delete` + findUnique prévio = 404 semântico + 204 na resposta
- Filhos primeiro, pai depois — em `$transaction` quando não há cascade
- Soft delete troca remoção por flag `deletadoEm` — toda leitura filtra
