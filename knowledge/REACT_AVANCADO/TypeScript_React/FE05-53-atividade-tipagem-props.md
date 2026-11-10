# FE05-53 — Atividade: Tipagem de Props no React

## Objetivo

Tipar um componente de card completo — props obrigatórias, opcionais, callbacks e children — e variantes com union types.

## O componente ProdutoCard

```tsx
interface Produto {
  id: number;
  nome: string;
  preco: number;
  imagem: string;
  descricao?: string;
}

interface ProdutoCardProps {
  produto: Produto;
  destaque?: boolean;
  onAdicionar: (id: number) => void;
  onRemover?: (id: number) => void;
  children?: ReactNode;
}

function ProdutoCard({
  produto,
  destaque = false,
  onAdicionar,
  onRemover,
  children
}: ProdutoCardProps) {
  return (
    <div className={`card ${destaque ? "destaque" : ""}`}>
      <img src={produto.imagem} alt={produto.nome} />
      <h3>{produto.nome}</h3>
      {produto.descricao && <p>{produto.descricao}</p>}
      <p>R$ {produto.preco.toFixed(2)}</p>
      <button onClick={() => onAdicionar(produto.id)}>
        Adicionar
      </button>
      {onRemover && (
        <button onClick={() => onRemover(produto.id)}>×</button>
      )}
      {children}
    </div>
  );
}
```

## Componente de botão com variantes

```tsx
interface BotaoProps extends React.ComponentProps<"button"> {
  variante: "primario" | "secundario" | "perigo" | "fantasma";
  tamanho?: "sm" | "md" | "lg";
  icone?: ReactNode;
}

function Botao({
  variante,
  tamanho = "md",
  icone,
  children,
  ...rest
}: BotaoProps) {
  return (
    <button className={`btn btn-${variante} btn-${tamanho}`} {...rest}>
      {icone}
      {children}
    </button>
  );
}
```

```tsx
// uso — autocomplete e validação
<Botao variante="primario" onClick={salvar} disabled={enviando}>
  Salvar
</Botao>

<Botao variante="perigo" tamanho="sm">Excluir</Botao>
<Botao variante="banana">Erro!</Botao> {/* ❌ erro de tipo */}
```

## Lista genérica — o desafio

```tsx
interface ListaProps<T> {
  itens: T[];
  carregando: boolean;
  erro?: string;
  renderItem: (item: T, index: number) => ReactNode;
  vazio?: ReactNode;
}

function Lista<T>({ itens, carregando, erro, renderItem, vazio }: ListaProps<T>) {
  if (carregando) return <p>Carregando...</p>;
  if (erro) return <p>{erro}</p>;
  if (itens.length === 0) return <>{vazio || "Nenhum item"}</>;

  return <ul>{itens.map(renderItem)}</ul>;
}
```

```tsx
// uso — T inferido como Produto
<Lista
  itens={produtos}
  carregando={carregando}
  renderItem={p => <ProdutoCard key={p.id} produto={p} onAdicionar={add} />}
/>
```

## O padrão — props de modal

```tsx
interface ModalProps {
  aberto: boolean;
  fechar: () => void;
  titulo: string;
  children: ReactNode;
  acoes?: ReactNode;
}

function Modal({ aberto, fechar, titulo, children, acoes }: ModalProps) {
  if (!aberto) return null;
  // ...
}
```

## Critérios de verificação

- `interface` para props — `type` se for union/complexa
- `ReactNode` para children
- Union types para variantes — autocomplete funciona
- `ComponentProps<"button">` para herdar props nativas
- Genérico `<T>` quando o tipo de item varia
- `key={...}` estável na lista

## Erros comuns

| Erro | Correção |
| --- | --- |
| `props: any` | `interface Props` — tipifique |
| `onClick: Function` | `() => void` ou `(e) => void` |
| Prop opcional sem `?` | `prop?: tipo` |
| Componente sem `children` | `ReactNode` ou `PropsWithChildren` |
| Union sem literal | `"a" \| "b"` — não `string` genérica |
