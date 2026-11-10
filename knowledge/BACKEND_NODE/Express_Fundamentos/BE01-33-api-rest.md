# BE01-33 — API REST

## O que é REST

**Representational State Transfer** — convenções para APIs HTTP:

```text
Recursos (URLs)  +  Verbos HTTP  +  Representações (JSON)
```

## Os 6 princípios essenciais

1. **Cliente-servidor** — separados, comunicação só via HTTP
2. **Stateless** — cada request carrega tudo que precisa; o servidor não lembra da anterior (o token vai em toda requisição)
3. **Cacheable** — respostas podem declarar se são cacheáveis
4. **Interface uniforme** — recursos identificados por URL, verbos padronizados
5. **Sistema em camadas** — cliente não sabe se fala com o servidor final ou com proxy/load balancer
6. **Code on demand** — opcional, quase nunca usado

## Modelagem REST — recursos, não ações

```text
❌ Ações na URL                    ✅ Recursos
POST /criarUsuario                 POST   /usuarios
GET  /buscarProdutos               GET    /produtos
POST /deletarPedido/5              DELETE /pedidos/5
GET  /obterUsuarioPorId/3          GET    /usuarios/3
```

E ações que não são CRUD?

```text
POST /pedidos/42/cancelar     — sub-ação (aceitável)
POST /auth/login              — recurso "sessão" criado
```

## Stateless na prática

```text
Request 1: POST /login          → { "token": "abc123" }
Request 2: GET /perfil
           Header: Authorization: Bearer abc123
```

O servidor não "lembra" que você logou — o token autentica **cada** request.

## Resposta REST típica

```json
// GET /usuarios/1
{
  "id": 1,
  "nome": "Ana",
  "email": "ana@email.com"
}

// Erro padronizado
{
  "message": "Usuário não encontrado",
  "statusCode": 404
}
```

## REST vs outras abordagens

| Abordagem | Modelo |
| --- | --- |
| **REST** | Recursos + verbos HTTP — o padrão |
| **GraphQL** | Um endpoint, cliente pede os campos que quer |
| **RPC/gRPC** | Chama funções remotas (`getUser(3)`) |

## Resumo

- REST = URLs são recursos, verbos HTTP são ações, JSON é a representação
- Stateless: cada request é independente — autenticação via token sempre
- Verbos na URL são anti-padrão REST
- Consistência: plural, status corretos, erro padronizado
