# FE05-56 — TypeScript no React: Inputs Componentizados

## O input base tipado

```tsx
interface InputProps {
  label: string;
  nome: string;
  tipo?: "text" | "email" | "password" | "number";
  placeholder?: string;
  erro?: string;
  register: UseFormRegisterReturn; // do react-hook-form
}

function Input({ label, nome, tipo = "text", placeholder, erro, register }: InputProps) {
  return (
    <div className={`campo ${erro ? "com-erro" : ""}`}>
      <label htmlFor={nome}>{label}</label>
      <input
        id={nome}
        type={tipo}
        placeholder={placeholder}
        {...register}
      />
      {erro && <span className="erro-msg">{erro}</span>}
    </div>
  );
}
```

## Com forwardRef — o ref passa

```tsx
import { forwardRef } from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  erro?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, erro, ...rest }, ref) {
    return (
      <div className={`campo ${erro ? "com-erro" : ""}`}>
        <label>{label}</label>
        <input ref={ref} {...rest} />
        {erro && <span>{erro}</span>}
      </div>
    );
  }
);
```

`InputHTMLAttributes` herda `placeholder`, `type`, `onChange`, etc.

## O Input com Hook Form — a integração

```tsx
function Formulario() {
  const { register, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });

  return (
    <>
      <Input
        label="Nome"
        register={register("nome")}
        erro={errors.nome?.message}
      />
      <Input
        label="Email"
        tipo="email"
        register={register("email")}
        erro={errors.email?.message}
      />
    </>
  );
}
```

## Select tipado

```tsx
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  opcoes: { valor: string; texto: string }[];
  erro?: string;
}

function Select({ label, opcoes, erro, ...rest }: SelectProps) {
  return (
    <div className={`campo ${erro ? "com-erro" : ""}`}>
      <label>{label}</label>
      <select {...rest}>
        {opcoes.map(o => (
          <option key={o.valor} value={o.valor}>{o.texto}</option>
        ))}
      </select>
      {erro && <span>{erro}</span>}
    </div>
  );
}
```

## Checkbox

```tsx
interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  erro?: string;
}

function Checkbox({ label, erro, ...rest }: CheckboxProps) {
  return (
    <label className="checkbox">
      <input type="checkbox" {...rest} />
      {label}
      {erro && <span>{erro}</span>}
    </label>
  );
}
```

## Agrupando — o formulário montado

```tsx
function Formulario() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input label="Nome" register={register("nome")} erro={errors.nome?.message} />
      <Input label="Email" register={register("email")} erro={errors.email?.message} />
      <Select
        label="Estado"
        opcoes={[{ valor: "SP", texto: "São Paulo" }]}
        {...register("estado")}
        erro={errors.estado?.message}
      />
      <button>Enviar</button>
    </form>
  );
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `register` passado errado | `{...register}` — desestruture o retorno |
| `ref` não chega no input | `forwardRef` no componente |
| `errors.x` sem `?.` | `errors.x?.message` — pode ser undefined |
| Props HTML não herdadas | `extends InputHTMLAttributes<HTMLInputElement>` |

## Resumo

- `forwardRef` + `InputHTMLAttributes` para inputs reutilizáveis
- `register` do Hook Form passa como prop `{...register}`
- `erro?: string` — mostra só quando existe
- Select/Checkbox herdam `SelectHTMLAttributes`/`InputHTMLAttributes`
