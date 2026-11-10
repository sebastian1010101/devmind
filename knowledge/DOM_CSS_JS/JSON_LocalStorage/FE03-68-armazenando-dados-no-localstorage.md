# FE03-68 — Armazenando Dados no LocalStorage

## O fluxo completo

Guardar dados no localStorage é sempre o mesmo padrão de três passos:

```javascript
// 1. Preparar o dado (objeto, array, primitivo)
const configuracoes = { tema: "escuro", fonte: 16, notificacoes: true };

// 2. Serializar para JSON
const texto = JSON.stringify(configuracoes);

// 3. Salvar
localStorage.setItem("config", texto);
```

E para recuperar:

```javascript
// 1. Ler a string
const texto = localStorage.getItem("config");

// 2. Parsear (com proteção)
const config = texto ? JSON.parse(texto) : null;

// 3. Usar
if (config) {
  aplicarTema(config.tema);
}
```

## Salvando tipos diferentes

### String simples

```javascript
localStorage.setItem("nome", "Ana");
localStorage.getItem("nome"); // "Ana" — sem JSON necessário
```

### Número — volta como string

```javascript
localStorage.setItem("pontos", 1500);
const pontos = Number(localStorage.getItem("pontos")); // 1500 (number)
// ou
const pontos2 = parseInt(localStorage.getItem("pontos"), 10);
```

### Booleano — cuidado com "false"

```javascript
localStorage.setItem("ativo", "false");
localStorage.getItem("ativo") === "true"; // false — string "false" é truthy!
```

```javascript
// ✅ Comparar com a string
const ativo = localStorage.getItem("ativo") === "true";

// ✅ Ou usar JSON
localStorage.setItem("ativo", JSON.stringify(false));
const ativo = JSON.parse(localStorage.getItem("ativo")); // false (boolean)
```

### Objeto

```javascript
const carrinho = { itens: [{ id: 1, qtd: 2 }], total: 150 };

localStorage.setItem("carrinho", JSON.stringify(carrinho));

const salvo = JSON.parse(localStorage.getItem("carrinho"));
console.log(salvo.itens.length); // 1
```

### Array

```javascript
const historico = ["produto-1", "produto-5", "produto-2"];

localStorage.setItem("historico", JSON.stringify(historico));

const lista = JSON.parse(localStorage.getItem("historico") || "[]");
// O fallback "[]" evita erro se a chave não existir
```

## Padrão utilitário: wrapper com fallback

Reutilizável em qualquer projeto — lê e grava com segurança:

```javascript
const storage = {
  get(chave, fallback = null) {
    try {
      const texto = localStorage.getItem(chave);
      return texto !== null ? JSON.parse(texto) : fallback;
    } catch {
      return fallback;
    }
  },

  set(chave, valor) {
    localStorage.setItem(chave, JSON.stringify(valor));
  },

  remove(chave) {
    localStorage.removeItem(chave);
  }
};

// Uso
storage.set("usuario", { nome: "Ana", nivel: 3 });
const user = storage.get("usuario", { nome: "Convidado" });
storage.remove("usuario");
```

## Atualizando dados existentes

Para modificar um objeto salvo, leia → altere → salve de volta:

```javascript
// Ler
const config = storage.get("config") || {};

// Alterar
config.tema = "escuro";
config.ultimoAcesso = new Date().toISOString();

// Salvar de volta
storage.set("config", config);
```

## Atualizando arrays — append seguro

```javascript
function adicionarHistorico(produtoId) {
  const historico = storage.get("historico") || [];

  // Evita duplicatas
  const filtrado = historico.filter(id => id !== produtoId);
  filtrado.unshift(produtoId); // mais recente primeiro

  // Limita a 20 itens
  const limitado = filtrado.slice(0, 20);

  storage.set("historico", limitado);
}
```

## Nomes de chave — boas práticas

```javascript
// ❌ Genérico demais
localStorage.setItem("dados", ...);
localStorage.setItem("x", ...);

// ✅ Namespaced e descritivo
localStorage.setItem("kenzieflix:usuario", ...);
localStorage.setItem("blog:config", ...);
localStorage.setItem("loja:carrinho", ...);
```

O prefixo `app:` evita colisões quando várias aplicações compartilham a mesma origem.

## Verificando quota e suporte

```javascript
// O navegador suporta localStorage?
if (typeof Storage !== "undefined") {
  // sim, pode usar
} else {
  // fallback — manter só em memória
}

// Estimativa de espaço usado (aproximada)
function tamanhoStorage() {
  let total = 0;
  for (let i = 0; i < localStorage.length; i++) {
    const chave = localStorage.key(i);
    total += chave.length + localStorage.getItem(chave).length;
  }
  return `~${(total / 1024).toFixed(1)} KB de ~5 MB`;
}
```

## Erros comuns

| Erro | Sintoma | Correção |
| --- | --- | --- |
| `setItem("x", {a:1})` sem stringify | `getItem` retorna `"[object Object]"` | `JSON.stringify` antes |
| `getItem` retorna `null` e chama `.prop` | `TypeError: Cannot read properties of null` | Verifique `!== null` ou use fallback |
| `getItem("ativo") === true` | Sempre falso — retorna string | `=== "true"` ou `JSON.parse` |
| `localStorage.clear()` em debug | Apaga TODAS as chaves da origem | Use `removeItem` para deletar uma só |
