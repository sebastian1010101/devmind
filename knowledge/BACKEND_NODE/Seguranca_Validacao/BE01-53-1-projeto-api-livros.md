# BE01-53-1 — Projeto: API de Livros

> **Status: [NO IMPLEMENT]** — anotações de referência sobre o escopo.

## Escopo esperado

Primeiro projeto consolidado do módulo — API REST completa de livros aplicando toda a arquitetura vista:

- CRUD completo de livros (título, autor, ano, etc.)
- Arquitetura em camadas: routes → controllers → services → database em memória
- `AppError` + middleware `handleErrors`
- Validação básica de entrada
- `app.ts`/`server.ts` separados

## Esqueleto de referência

```typescript
interface Livro {
  id: number;
  titulo: string;
  autor: string;
  ano: number;
}
```

```text
GET    /livros       → lista
GET    /livros/:id   → busca
POST   /livros       → cria (201)
PATCH  /livros/:id   → atualiza
DELETE /livros/:id   → remove (204)
```

A **Parte 2** (BE01-63-1) adiciona validação com Zod + middlewares de validação sobre a mesma API.

## Resumo

- Projeto marco — consolida arquitetura, erros e CRUD
- Parte 2 refina com Zod — validação em middleware
- Não implementado — referência para consulta futura
