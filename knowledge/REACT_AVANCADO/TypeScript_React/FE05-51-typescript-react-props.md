# FE05-51 — TypeScript no React: Props

## Tipando props com interface

```tsx
interface CardProps {
  titulo: string;
  descricao: string;
  imagem?: string;        // opcional
  destaque?: boolean;
}

function Card({ titulo, descricao, imagem, destaque }: CardProps) {
  return (
    <div className={destaque ? "card destaque" : "card"}>
      {imagem && <img src={imagem} />}
      <h3>{titulo}</h3>
      <p>{descricao}</p>
    </div>
  );
}
```

## children — ReactNode

```tsx
interface LayoutProps {
  children: ReactNode; // aceita qualquer JSX
  titulo?: string;
}

function Layout({ children, titulo }: LayoutProps) {
  return (
    <div>
      {titulo && <h1>{titulo}</h1>}
      {children}
    </div>
  );
}
```

## Props de função — callbacks tipados

```tsx
interface BotaoProps {
  texto: string;
  onClick: () => void;                    // sem args
  onMudar?: (valor: string) => void;      // com arg
  onEnviar?: (dados: FormData) => Promise<void>; // async
}
```

## Props com união — componente que muda

```tsx
interface BotaoProps {
  variante: "primario" | "secundario" | "perigo";
  tamanho?: "sm" | "md" | "lg";
}

function Botao({ variante, tamanho = "md" }: BotaoProps) {
  return <button className={`btn ${variante} ${tamanho}`} />;
}
```

## Props opcionais vs default

```tsx
// Opcional — pode não vir
interface Props {
  onClick?: () => void;
}

// Default — vem com valor se não passar
function Botao({ tamanho = "md" }: { tamanho?: string }) {
  // tamanho é sempre "sm" | "md" | "lg" — default garante
}
```

## Extends — props que herdam

```tsx
interface ElementoBase {
  id: string;
  className?: string;
}

interface CardProps extends ElementoBase {
  titulo: string;
}
```

## O caso do style — CSSProperties

```tsx
interface BoxProps {
  cor: string;
  children: ReactNode;
}

function Box({ cor, children }: BoxProps) {
  const estilo: CSSProperties = {
    backgroundColor: cor,
    padding: "1rem"
  };
  return <div style={estilo}>{children}</div>;
}
```

## Componente genérico — props com T

```tsx
interface ListaProps<T> {
  itens: T[];
  renderItem: (item: T) => ReactNode;
}

function Lista<T>({ itens, renderItem }: ListaProps<T>) {
  return <ul>{itens.map(renderItem)}</ul>;
}

// uso — T inferido
<Lista
  itens={produtos}
  renderItem={p => <li key={p.id}>{p.nome}</li>}
/>
```

## Props de HTML nativos — ComponentProps

```tsx
// Herda todas as props de <button>
interface BotaoProps extends React.ComponentProps<"button"> {
  variante: "primario" | "secundario";
}

function Botao({ variante, ...rest }: BotaoProps) {
  return <button className={variante} {...rest} />;
}

// aceita: onClick, disabled, type, etc. — todas nativas
<Botao variante="primario" onClick={...} disabled type="submit" />
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `children` sem tipo | `ReactNode` — qualquer JSX |
| `onClick: Function` | `() => void` ou `(e: MouseEvent) => void` |
| Props com `any` | `interface` ou `ComponentProps` |
| `React.FC` mascarando children | `interface Props { children: ReactNode }` |

## Resumo

- `interface Props` define o contrato do componente
- `ReactNode` para children; callbacks tipados com parâmetros
- Union types para variantes (`"primario" | "secundario"`)
- `ComponentProps<"button">` herda props nativas
