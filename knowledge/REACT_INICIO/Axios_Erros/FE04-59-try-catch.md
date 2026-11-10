# FE04-59 — Try-Catch

## Por que tratar erros

Toda requisição pode falhar: rede cai, servidor retorna 500, JSON quebra, usuário cancela. Sem tratamento, o app trava ou mostra tela em branco.

```javascript
try {
  const res = await api.get("/produtos");
  setProdutos(res.data);
} catch (erro) {
  setErro(erro); // captura e trata
} finally {
  setCarregando(false); // roda SEMPRE — sucesso ou falha
}
```

## A anatomia do try/catch/finally

```javascript
try {
  // código que pode falhar
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  const dados = await res.json();
  setDados(dados);
} catch (e) {
  // só roda se try lançou algo
  setErro(e.message);
} finally {
  // roda SEMPRE — try ou catch
  setCarregando(false);
}
```

## Os tipos de erro

### 1. Erro de rede (fetch/axios não chegou no servidor)

```javascript
// fetch: TypeError "Failed to fetch"
// axios: erro sem response — erro.request existe, erro.response não

if (erro.request && !erro.response) {
  setErro("Sem conexão — verifique sua internet");
}
```

### 2. Erro HTTP (servidor respondeu com 4xx/5xx)

```javascript
// fetch: res.ok é false
if (!res.ok) throw new Error(`Erro ${res.status}`);

// axios: lança automaticamente — erro.response tem o status
if (erro.response?.status === 404) {
  setErro("Recurso não encontrado");
} else if (erro.response?.status === 500) {
  setErro("Erro no servidor — tente mais tarde");
}
```

### 3. Erro de dados (JSON inválido, campo esperado ausente)

```javascript
try {
  const dados = await res.json(); // quebra se JSON malformado
} catch (e) {
  setErro("Resposta inválida do servidor");
}
```

### 4. Erro de lógica (seu próprio throw)

```javascript
if (dados.erro) { // caso do ViaCEP
  throw new Error("CEP não encontrado");
}
```

## O objeto erro do Axios

```javascript
catch (erro) {
  erro.response          // resposta HTTP (se existir)
  erro.response.status   // 404, 500...
  erro.response.data     // body do erro — mensagens da API
  erro.request           // requisição feita (sem resposta = rede)
  erro.message           // mensagem genérica
  erro.code              // 'ECONNABORTED' (timeout), 'ERR_NETWORK'
}
```

```javascript
catch (erro) {
  if (erro.response) {
    // Servidor respondeu com erro
    setErro(erro.response.data?.message || `Erro ${erro.response.status}`);
  } else if (erro.request) {
    // Requisição saiu mas sem resposta
    setErro("Sem resposta do servidor — verifique a conexão");
  } else {
    // Erro na montagem da requisição
    setErro(erro.message);
  }
}
```

## Erros amigáveis — traduzindo pro usuário

```javascript
function mensagemErro(erro) {
  if (erro.code === "ECONNABORTED") return "Tempo esgotado — tente de novo";
  if (erro.code === "ERR_NETWORK") return "Sem conexão com a internet";

  const status = erro.response?.status;
  if (status === 400) return "Dados inválidos";
  if (status === 401) return "Faça login novamente";
  if (status === 403) return "Sem permissão";
  if (status === 404) return "Não encontrado";
  if (status >= 500) return "Servidor indisponível";

  return erro.message || "Erro inesperado";
}
```

## O padrão completo

```jsx
const [dados, setDados] = useState(null);
const [carregando, setCarregando] = useState(false);
const [erro, setErro] = useState(null);

async function carregar() {
  setCarregando(true);
  setErro(null);

  try {
    const res = await api.get("/produtos");
    setDados(res.data);
  } catch (e) {
    setErro(mensagemErro(e));
  } finally {
    setCarregando(false);
  }
}

// mostrar
{carregando && <p>Carregando...</p>}
{erro && <p className="erro">{erro} <button onClick={carregar}>Tentar de novo</button></p>}
{dados && <Lista dados={dados} />}
```

## Retry automático — tentando de novo

```javascript
async function carregarComRetry(tentativas = 3) {
  for (let i = 0; i < tentativas; i++) {
    try {
      return await api.get("/produtos");
    } catch (e) {
      if (i === tentativas - 1) throw e; // última tentativa — propaga
      await new Promise(r => setTimeout(r, 1000 * (i + 1))); // espera
    }
  }
}
```

## Onde NÃO usar try/catch

```javascript
// ❌ Erros de render não são pegos por try/catch
// Use Error Boundary (componentDidCatch / react-error-boundary)

// ❌ Erros em callbacks de evento fora do render
// precisam de seu próprio try/catch
button.onclick = async () => {
  try { await acao() } catch (e) { /* trata */ }
};
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `try` sem mostrar nada no `catch` | Sempre dê feedback — `setErro` ou toast |
| `finally` esquecido | Loading nunca desliga |
| Catch genérico sem tipo | Diferencie rede vs HTTP vs dados |
| `throw` sem mensagem útil | `new Error("descrição clara")` |
| `try` cobrindo código demais | Envolva só o que pode falhar |

## Resumo

- `try/catch/finally` isola falhas de rede, HTTP e parse
- Axios dá `erro.response` (HTTP), `erro.request` (rede), `erro.code` (timeout)
- Traduza erros para mensagens amigáveis
- Loading sempre desliga no `finally`
- Error Boundary para erros de render — try/catch não pega JSX
