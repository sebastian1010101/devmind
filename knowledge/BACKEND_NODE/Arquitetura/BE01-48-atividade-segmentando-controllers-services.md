# BE01-48 — Atividade: Segmentando Controllers e Services

Exercício: separar de vez — controller só traduz HTTP, service só faz regra.

## O código "antes" — tudo no handler

```typescript
// ❌ controller gordo — valida, regra, acesso a dados, resposta
app.post("/usuarios", (req, res) => {
  const { nome, email, senha } = req.body;
  if (!nome || !email || !senha) {
    return res.status(400).json({ message: "Campos obrigatórios" });
  }
  if (usuarios.some((u) => u.email === email)) {
    return res.status(409).json({ message: "Email já cadastrado" });
  }
  const usuario = { id: proximoId++, nome, email, senha };
  usuarios.push(usuario);
  const { senha: _, ...publico } = usuario;
  res.status(201).json(publico);
});
```

## Depois — cada camada no seu lugar

```typescript
// service — regra pura, retorna ou lança
class UsuarioService {
  criar(dados: CriarUsuarioDTO): Usuario {
    if (this.repo.buscarPorEmail(dados.email)) {
      throw new AppError("Email já cadastrado", 409);
    }
    return this.repo.criar(dados);
  }
}
```

```typescript
// controller — extrai, chama, responde
class UsuarioController {
  constructor(private service: UsuarioService) {}

  criar = (req: Request, res: Response) => {
    const usuario = this.service.criar(req.body);
    const { senha, ...publico } = usuario;
    return res.status(201).json(publico);
  };
}
```

```typescript
// route — só liga endpoint ao controller
router.post("/", controller.criar);
```

## A divisão das responsabilidades

| Antes (handler único) | Depois |
| --- | --- |
| Validação de presença | Middleware de validação (Zod, BE01-58) |
| Email duplicado | Service (regra de negócio) |
| `usuarios.push` | Repository (dados) |
| `res.status(201)` | Controller (HTTP) |
| Remover senha | Controller (formato da resposta) |

## Ganho imediato

```typescript
// Testar a regra sem Express, sem porta, sem HTTP
const service = new UsuarioService(new RepoMemoria());
service.criar({ nome: "Ana", email: "a@b.com", senha: "x" });
service.criar({ nome: "Ana", email: "a@b.com", senha: "x" });
// → AppError: Email já cadastrado ✅
```

## Checklist

- [ ] Controller tem ~5 linhas por método
- [ ] Service não importa nada do Express
- [ ] Erros de negócio lançados (`throw`), não retornados
- [ ] Campo sensível (senha) removido na resposta
- [ ] Rota é uma linha: `router.post("/", controller.criar)`

## Resumo

- Controller gordo vira: middleware (valida) → controller (HTTP) → service (regra) → repo (dados)
- Remover `senha` da resposta é responsabilidade do controller — formato de saída
- Service testável sem servidor rodando
