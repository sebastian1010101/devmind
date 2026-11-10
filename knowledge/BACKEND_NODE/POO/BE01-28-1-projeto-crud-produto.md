# BE01-28-1 — Projeto: CRUD de Produto

> **Status: [NO IMPLEMENT]** — anotações de referência sobre o escopo do projeto.

## Escopo esperado

Consolidar POO + TypeScript num CRUD de produtos completo (ainda sem Express):

- Classe `Produto` com construtor validado e campos privados
- Classe `EstoqueService`/`ProdutoRepository` com as 4 operações
- Interfaces para o contrato do repositório
- Tipos derivados (`Omit`, `Partial`) para DTOs
- Herança de `Error` para erros de domínio (`ProdutoNaoEncontradoError`)

## Esqueleto de referência

```typescript
interface IProduto {
  id: number;
  nome: string;
  preco: number;
  estoque: number;
}

type CriarProdutoDTO = Omit<IProduto, "id">;
type AtualizarProdutoDTO = Partial<CriarProdutoDTO>;

interface IProdutoRepository {
  criar(dados: CriarProdutoDTO): IProduto;
  buscarPorId(id: number): IProduto | undefined;
  listar(): IProduto[];
  atualizar(id: number, dados: AtualizarProdutoDTO): IProduto | undefined;
  deletar(id: number): boolean;
}
```

Este projeto vira a base da API Express nos próximos blocos — o mesmo CRUD, agora exposto via HTTP.

## Resumo

- Projeto marco da seção POO — não implementado, apenas referência
- Consolida: classes, interfaces, herança de Error, DTOs derivados
- Reaparece como API real em BE01-52 (Cars API) e projetos posteriores
