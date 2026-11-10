# BE02-66 — Utilizando JWT — Parte 4

## Expiração na prática

```ts
// access token curto — segurança
expiresIn: "15m"
```

Token roubado é válido até expirar — `exp` curto limita o dano. Mas relogar a cada 15 min é péssimo UX → **refresh token**.

## Refresh token — o par

```text
login → { accessToken: "15m", refreshToken: "7d" }

accessToken expira → POST /refresh { refreshToken }
                  → servidor valida → novo accessToken
```

```ts
const accessToken = jwt.sign(payload, SECRET, { subject: id, expiresIn: "15m" });
const refreshToken = jwt.sign({ type: "refresh" }, SECRET, {
  subject: id,
  expiresIn: "7d",
});
```

```ts
router.post("/refresh", async (req, res) => {
  try {
    const payload = jwt.verify(req.body.refreshToken, SECRET) as JwtPayload;
    if (payload.type !== "refresh") throw new Error();

    const novo = jwt.sign({}, SECRET, {
      subject: payload.sub,
      expiresIn: "15m",
    });
    return res.json({ accessToken: novo });
  } catch {
    return res.status(401).json({ message: "Refresh inválido" });
  }
});
```

Refresh tokens devem ser **armazenados no banco** (ou rotacionados) para permitir revogação.

## O problema do logout

JWT é stateless — não existe "desligar" um token emitido:

| Estratégia | Como |
| --- | --- |
| `exp` curto | Token morre rápido — logout só descarta no cliente |
| Blacklist | Redis/tabela com tokens revogados — checa no middleware |
| Rotacionar segredo | Invalida **todos** — logout global |

```ts
// blacklist simples
await prisma.tokenRevogado.create({ data: { jti: payload.jti } });
// middleware checa: payload.jti está na lista? → 401
```

## Claims customizados

```ts
const token = jwt.sign(
  { role: usuario.role },          // claim custom
  SECRET,
  { subject: id }
);

// middleware de autorização por papel
function requireRole(role: string) {
  return (req, res, next) => {
    if (res.locals.role !== role) {
      return res.status(403).json({ message: "Sem permissão" });
    }
    next();
  };
}
```

`role` no token evita query a cada request — mas mudança de papel só vale no próximo token.

## Boas práticas finais

- `exp` curto no access, refresh separado
- `sub` para id; claims mínimos no payload
- HTTPS sempre — token é credencial
- Secret forte + no `.env`; rotacione se vazar
- Não confie no payload sem `verify` — `decode` não valida

## Erros comuns

| Erro | Correção |
| --- | --- |
| Access token com `exp` longo | Curto (`15m`) + refresh |
| Refresh token sem revogação | Guarde no banco — delete no logout |
| `role` do token desatualizado | Aceite o delay ou valide no banco nas rotas críticas |
| Blacklist em memória | Reiniciou = perdeu — Redis/tabela persiste |

## Resumo

- Access curto + refresh longo é o padrão de sessão
- Logout real exige blacklist ou revogação de refresh — stateless tem custo
- Claims custom (`role`) autorizam sem query — com trade-off de frescor
- `decode` lê, `verify` valida — nunca confunda
