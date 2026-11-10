# BE01-16 — Atividade: Função de Cadastro de Produtos

Aplicar interfaces e tipos num CRUD simplificado de produtos.

## Estrutura

```typescript
enum Categoria {
  Eletronicos = "ELETRONICOS",
  Alimentos = "ALIMENTOS",
  Vestuario = "VESTUARIO",
}

interface Produto {
  id: number;
  nome: string;
  preco: number;
  categoria: Categoria;
  estoque: number;
}

interface CriarProdutoDTO {
  nome: string;
  preco: number;
  categoria: Categoria;
  estoque?: number; // padrão 0
}
```

## Implementação

```typescript
const estoque: Produto[] = [];
let proximoId = 1;

function cadastrarProduto(dados: CriarProdutoDTO): Produto {
  const produto: Produto = {
    id: proximoId++,
    estoque: 0,
    ...dados,
  };
  estoque.push(produto);
  return produto;
}

function listarPorCategoria(categoria: Categoria): Produto[] {
  return estoque.filter((p) => p.categoria === categoria);
}

function valorTotalEmEstoque(): number {
  return estoque.reduce((total, p) => total + p.preco * p.estoque, 0);
}
```

## Testando

```typescript
cadastrarProduto({ nome: "Mouse", preco: 79.9, categoria: Categoria.Eletronicos, estoque: 15 });
cadastrarProduto({ nome: "Arroz 5kg", preco: 32.5, categoria: Categoria.Alimentos, estoque: 40 });
cadastrarProduto({ nome: "Camiseta", preco: 49.9, categoria: Categoria.Vestuario });

console.log(listarPorCategoria(Categoria.Eletronicos));
console.log(`Total: R$ ${valorTotalEmEstoque().toFixed(2)}`);
```

## Desafios extras

1. `buscarPorNome(termo: string): Produto[]` — filtro case-insensitive com `includes`
2. `atualizarEstoque(id: number, quantidade: number): boolean` — soma/subtrai, sem ficar negativo
3. `relatorio()` — retorna `{ totalProdutos, valorTotal, porCategoria: Record<Categoria, number> }`
4. Validação: `cadastrarProduto` rejeita `preco <= 0` ou `nome` vazio

## Checklist

- [ ] DTO separado da entidade (sem `id` na entrada)
- [ ] Enum para categoria — sem strings soltas
- [ ] `estoque` com default via spread ordenado
- [ ] Funções com retorno tipado
- [ ] `Partial`/`Omit` onde faz sentido

## Resumo

- Entidade `Produto` vs `CriarProdutoDTO` — contratos distintos
- Enum + interface + union types juntos num exercício real
- `...dados` depois do default permite override opcional
