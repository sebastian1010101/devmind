# FE05-58 — TypeScript no React: Axios

## Axios tipado — a resposta

```tsx
import axios from "axios";

interface Usuario {
  id: number;
  nome: string;
  email: string;
}

// api.get<T> — o tipo do body da resposta
const res = await api.get<Usuario[]>("/usuarios");
// res.data é Usuario[] — tipado!

res.data.map(u => u.nome); // ✅ autocomplete funciona
```

## A instância com tipos

```tsx
// services/api.ts
import axios from "axios";

export const api = axios.create({
  baseURL: "https://api.exemplo.com",
  timeout: 8000
});

// funções tipadas do serviço
export const usuariosApi = {
  listar: () => api.get<Usuario[]>("/usuarios").then(r => r.data),
  buscar: (id: number) => api.get<Usuario>(`/usuarios/${id}`).then(r => r.data),
  criar: (dados: Omit<Usuario, "id">) => api.post<Usuario>("/usuarios", dados).then(r => r.data),
  atualizar: (id: number, dados: Partial<Usuario>) => api.put<Usuario>(`/usuarios/${id}`, dados).then(r => r.data),
  remover: (id: number) => api.delete(`/usuarios/${id}`)
};
```

## O erro tipado — AxiosError

```tsx
import axios, { AxiosError } from "axios";

try {
  await api.get("/dados");
} catch (e) {
  if (axios.isAxiosError(e)) {
    // e é AxiosError — tem response, request, code
    console.log(e.response?.status);
    console.log(e.response?.data);
  }
}
```

## Erro com resposta tipada

```tsx
interface ErroApi {
  message: string;
  campo?: string;
}

catch (e) {
  if (axios.isAxiosError<ErroApi>(e)) {
    const dados = e.response?.data; // ErroApi | undefined
    setErro(dados?.message || "Erro");
  }
}
```

## POST/PUT/PATCH tipados

```tsx
// body vai tipado, resposta vem tipada
const res = await api.post<Usuario>("/usuarios", {
  nome: "Ana",
  email: "ana@email.com"
});
// res.data é Usuario — com id

// body errado → erro de compilação
api.post("/usuarios", { nome: "Ana" }); // ❌ falta email se obrigatório
```

## Params tipados

```tsx
interface Filtros {
  categoria?: string;
  pagina?: number;
  busca?: string;
}

const res = await api.get<Produto[]>("/produtos", {
  params: {
    categoria: "eletronicos",
    pagina: 2
  } satisfies Filtros // valida o objeto
});
```

## Interceptor com tipos

```tsx
api.interceptors.request.use(config => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

## O hook genérico com axios

```tsx
function useApi<T>(url: string) {
  const [dados, setDados] = useState<T | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    api.get<T>(url)
      .then(res => setDados(res.data))
      .catch(e => {
        if (axios.isAxiosError(e)) {
          setErro(e.response?.data?.message || e.message);
        }
      })
      .finally(() => setCarregando(false));
  }, [url]);

  return { dados, carregando, erro };
}

// uso
const { dados: produtos } = useApi<Produto[]>("/produtos");
// produtos: Produto[] | null
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `res.data` sem tipo | `api.get<T>` — dados tipados |
| `catch (e)` com `e: any` | `axios.isAxiosError(e)` — narrowing |
| `res.data.message` sem tipo | `AxiosError<ErroApi>` — resposta de erro tipada |
| Body sem validação | `Omit<Usuario, "id">` — sem id no create |

## Resumo

- `api.get<T>`/`post<T>`/`put<T>` — resposta tipada
- `AxiosError<TErro>` — erro tipado com `isAxiosError`
- `Omit`/`Partial` para bodies de create/update
- Hook `useApi<T>` — fetch genérico e tipado
