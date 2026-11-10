# FE05-55 — TypeScript no React: Zod e Hook Form

## React Hook Form — formulários performáticos

```bash
npm install react-hook-form
```

```tsx
import { useForm } from "react-hook-form";

interface FormData {
  nome: string;
  email: string;
  idade: number;
}

function Formulario() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>();

  function onSubmit(dados: FormData) {
    console.log(dados); // tipado!
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("nome")} />
      <input type="email" {...register("email")} />
      <input type="number" {...register("idade")} />
      <button>Enviar</button>
    </form>
  );
}
```

`register` conecta o input ao formulário — sem `useState` por campo.

## Zod — validação com tipos

```bash
npm install zod @hookform/resolvers
```

```tsx
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

const schema = z.object({
  nome: z.string().min(3, "Mínimo 3 caracteres"),
  email: z.string().email("Email inválido"),
  idade: z.number().min(18, "Precisa ser maior de 18").max(120)
});

// o tipo sai do schema — nunca dessincroniza
type FormData = z.infer<typeof schema>;
```

## Juntando — o padrão completo

```tsx
function Formulario() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<FormData>({
    resolver: zodResolver(schema)
  });

  async function onSubmit(dados: FormData) {
    await api.post("/usuarios", dados);
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("nome")} />
      {errors.nome && <span>{errors.nome.message}</span>}

      <input type="email" {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="number" {...register("idade", { valueAsNumber: true })} />
      {errors.idade && <span>{errors.idade.message}</span>}

      <button disabled={isSubmitting}>Enviar</button>
    </form>
  );
}
```

## Zod — o poder dos refinamentos

```tsx
const schema = z.object({
  email: z.string().email(),
  senha: z.string().min(8, "Mínimo 8"),
  confirmar: z.string(),
  cep: z.string().regex(/^\d{5}-?\d{3}$/, "CEP inválido"),
  nascimento: z.date().max(new Date(), "No futuro?"),
  tags: z.array(z.string()).min(1, "Pelo menos uma")
}).refine(d => d.senha === d.confirmar, {
  message: "Senhas não conferem",
  path: ["confirmar"]
});
```

## O tipo sai do schema — inferência

```tsx
// sem Zod — manual, pode dessincronizar
interface FormData {
  nome: string;
  email: string;
}

// com Zod — automático
const schema = z.object({ nome: z.string(), email: z.string().email() });
type FormData = z.infer<typeof schema>;
```

## watch e getValues — lendo fora do submit

```tsx
const { watch, getValues } = useForm<FormData>();

const senha = watch("senha");          // re-render a cada mudança
const atual = getValues();             // lê sem re-render
const todos = watch();                 // observa tudo
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `register` sem nome | `register("nome")` — conecta ao campo |
| `valueAsNumber` esquecido | Input retorna string — `{ valueAsNumber: true }` |
| `errors.campo` sem checar | `errors.campo?.message` — pode ser undefined |
| Schema fora do componente | Declare fora — não recria a cada render |

## Resumo

- `useForm<FormData>` tipa o formulário; `register` conecta os campos
- Zod valida e gera o tipo — `z.infer<typeof schema>`
- `zodResolver` liga o schema ao Hook Form
- `errors` tipados — `errors.nome.message`
