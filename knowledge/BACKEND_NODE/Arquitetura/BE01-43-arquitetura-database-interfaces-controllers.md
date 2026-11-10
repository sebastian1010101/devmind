# BE01-43 — Arquitetura: Database, Interfaces e Controllers

## Por que arquitetura

Rota com lógica dentro funciona — até o projeto crescer:

```typescript
// ❌ tudo misturado — impossível testar, reutilizar ou manter
app.post("/produtos", (req, res) => {
  const { nome, preco } = req.body;
  if (preco <= 0) return res.status(400).json({ message: "inválido" });
  produtos.push({ id: proximoId++, nome, preco });
  res.status(201).json(/* ... */);
});
```

## As camadas

```text
HTTP Request
    ↓
┌─────────────┐  recebe req, extrai dados, chama service, monta res
│ Controller  │  — SÓ fala HTTP (req/res, status, json)
└─────────────┘
    ↓
┌─────────────┐  regras de negócio — não conhece HTTP
│   Service   │  — recebe dados já extraídos, retorna resultado
└─────────────┘
    ↓
┌─────────────┐  acesso a dados — interface + implementação
│ Repository /│  — hoje array em memória, amanhã Prisma
│  Database   │
└─────────────┘
```

## O contrato entre camadas

```typescript
// interface do repositório — a fronteira
interface IProdutoRepository {
  criar(dados: CriarProdutoDTO): Produto;
  buscarPorId(id: number): Produto | undefined;
}

// service depende da interface, não da implementação
class ProdutoService {
  constructor(private repo: IProdutoRepository) {}

  criar(dados: CriarProdutoDTO): Produto {
    if (dados.preco <= 0) throw new AppError("Preço inválido");
    return this.repo.criar(dados);
  }
}

// controller só traduz HTTP ↔ service
class ProdutoController {
  constructor(private service: ProdutoService) {}

  criar = (req: Request, res: Response) => {
    const produto = this.service.criar(req.body);
    return res.status(201).json(produto);
  };
}
```

## A responsabilidade de cada camada

| Camada | Sabe de HTTP? | Sabe do banco? | Faz |
| --- | --- | --- | --- |
| Route | ✅ | ❌ | liga método+path ao controller |
| Controller | ✅ | ❌ | extrai req, chama service, monta res |
| Service | ❌ | ❌ | regras de negócio puras |
| Repository | ❌ | ✅ | persistência |

Controller nunca tem `if` de negócio; service nunca vê `req`/`res`.

## O ganho

- **Testável** — testa o service com repo fake, sem subir HTTP
- **Substituível** — troca array por Prisma implementando a interface
- **Legível** — cada arquivo faz uma coisa

## Resumo

- Controller traduz HTTP; Service executa regra; Repository persiste
- Interfaces são as fronteiras — dependa delas, não de implementações
- Camada fina em cima chama camada gorda embaixo, nunca o contrário
