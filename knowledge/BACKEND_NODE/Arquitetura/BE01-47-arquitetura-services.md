# BE01-47 — Arquitetura: Services

## O que é a camada Service

Onde mora a **regra de negócio** — o que o sistema faz, independente de HTTP:

```text
Controller: "recebi um POST /produtos com body X"
Service:    "criar produto exige preço > 0 e nome único"
Repository: "salvar isso no banco"
```

## Service não conhece Express

```typescript
// ✅ puro — testável sem subir servidor
class ProdutoService {
  criar(dados: CriarProdutoDTO): Produto {
    if (dados.preco <= 0) {
      throw new AppError("Preço deve ser positivo");
    }
    return this.repo.criar(dados);
  }
}
```

```typescript
// ❌ service vendo req/res — acoplado ao HTTP
class ProdutoService {
  criar(req: Request, res: Response) { /* ... */ }
}
```

Se precisar de `req` no service, algo está na camada errada.

## O que vai no service

- Validações de negócio (preço > 0, estoque suficiente, email único)
- Orquestração (criar pedido → debitar estoque → emitir nota)
- Regras condicionais (desconto por categoria, cálculo de frete)
- Decisões que geram erros de domínio (`throw new AppError`)

## O que NÃO vai no service

- `req.params`, `req.body` — extração é do controller
- `res.status()`, `res.json()` — resposta é do controller
- SQL/queries diretas — persistência é do repository
- Parsing de body — é de middleware

## Injeção de dependência manual

```typescript
class ProdutoService {
  constructor(private repo: IProdutoRepository) {}
}

// Em produção
const service = new ProdutoService(new ProdutoRepositoryPrisma());

// Em teste
const service = new ProdutoService(new ProdutoRepositoryMemoria());
```

O service recebe a **abstração** — troca o banco sem tocar na regra.

## Exemplo completo

```typescript
class PedidoService {
  constructor(
    private pedidoRepo: IPedidoRepository,
    private produtoRepo: IProdutoRepository
  ) {}

  criar(clienteId: number, itens: ItemDTO[]): Pedido {
    // Regra de negócio: verifica estoque de cada item
    for (const item of itens) {
      const produto = this.produtoRepo.buscar(item.produtoId);
      if (!produto) throw new AppError(`Produto ${item.produtoId} não existe`, 404);
      if (produto.estoque < item.qtd) {
        throw new AppError(`Estoque insuficiente: ${produto.nome}`);
      }
    }
    // Orquestração
    const pedido = this.pedidoRepo.criar({ clienteId, itens });
    itens.forEach((i) => this.produtoRepo.debitarEstoque(i.produtoId, i.qtd));
    return pedido;
  }
}
```

## Service vs Controller — teste rápido

```text
"Se essa regra valesse também para uma CLI ou um job agendado,
ela é do service — não do controller."
```

## Resumo

- Service = regra de negócio pura — zero Express, zero SQL
- Recebe dados extraídos, retorna resultado ou lança erro de domínio
- Depende de interfaces — injeção manual no construtor
- O teste: funcionaria num contexto sem HTTP? Então é service
