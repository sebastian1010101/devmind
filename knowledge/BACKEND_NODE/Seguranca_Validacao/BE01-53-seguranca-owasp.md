# BE01-53 — Segurança de Aplicações e OWASP

## O que é OWASP

**Open Web Application Security Project** — comunidade que cataloga as vulnerabilidades mais comuns. O **OWASP Top 10** é a referência: as 10 falhas mais exploradas em aplicações web.

## As vulnerabilidades que tocam uma API Node

### 1. Injection (SQL, NoSQL, comandos)

```typescript
// ❌ concatenação — usuário digita "'; DROP TABLE users; --"
db.query(`SELECT * FROM users WHERE email = '${email}'`);

// ✅ parâmetros — o banco trata o valor como dado, nunca como código
db.query("SELECT * FROM users WHERE email = $1", [email]);
// Prisma faz isso automaticamente — nunca monte SQL com template string
```

### 2. Broken Authentication

- Senhas em texto plano → sempre `bcrypt`/`argon2`, nunca o hash cru
- Tokens sem expiração → JWT com `expiresIn`
- Força bruta → rate limiting no `/login`

### 3. Sensitive Data Exposure

```text
❌ Stack trace na resposta de erro
❌ Senha no JSON de resposta (Omit<Usuario, "senha">)
❌ Segredos no código/git → .env + gitignore
❌ Console.log com dados de usuários em produção
```

### 4. Broken Access Control

```text
Usuário autenticado ≠ usuário autorizado

DELETE /usuarios/42 — qualquer um logado pode deletar qualquer um?
→ verificar: é dono do recurso OU é admin
```

### 5. Security Misconfiguration

- Headers default do Express (`X-Powered-By: Express` anuncia a stack)
- CORS `*` em produção
- Debug/logs verbosos ligados
- Dependências desatualizadas (`npm audit`)

### 6. XSS (quando o backend serve HTML)

Sanitizar entrada antes de salvar/renderizar — em APIs JSON é menos crítico, mas dados maliciosos salvos explodem no frontend de quem consome.

### 7. Falta de validação de entrada

```typescript
// confiar cegamente no body = abrir a porta
req.body.preco = "0.1 OR 1=1";  // sem validação, vai pro banco
```

Zod (BE01-56) valida na borda — rejeita antes de chegar na regra.

## Defesa em profundidade

```text
Camadas independentes — se uma falha, a outra segura:

1. Validação de entrada (Zod)
2. Headers seguros (Helmet)
3. Autenticação (JWT) + autorização (roles)
4. Queries parametrizadas (Prisma/ORM)
5. Hash de senha (bcrypt)
6. Rate limiting
7. Logs e monitoramento
```

## Checklist mínimo para uma API

- [ ] Nunca concatenar SQL — sempre parâmetros/ORM
- [ ] Senha → bcrypt, nunca comparável em texto
- [ ] Resposta nunca contém senha/segredos
- [ ] `helmet()` e `cors()` configurados
- [ ] 500 sem detalhes internos
- [ ] `npm audit` no CI

## Resumo

- OWASP Top 10 = o catálogo das falhas mais exploradas
- Injection: parâmetros sempre, concatenação nunca
- Autenticado ≠ autorizado — verifique ownership
- Defesa em camadas: validação + helmet + auth + ORM + hash
