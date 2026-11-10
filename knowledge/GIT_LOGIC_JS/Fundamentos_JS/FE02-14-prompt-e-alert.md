# FE02-14 — Prompt e Alert

## Métodos Nativos de Interação no Navegador

Antes de manipular formulários HTML complexos com o DOM, o JavaScript oferece funções globais integradas ao objeto `window` do navegador para exibir avisos rápidos e capturar dados do usuário:

---

## 1. `alert()` — Exibição de Avisos

Abre uma janela modal sutil com uma mensagem de texto e um botão "OK":

```javascript
alert("Atenção: sua sessão irá expirar em 5 minutos!");
```

- **Comportamento Bloqueante:** o `alert()` pausa completamente a execução de todo o código JavaScript da página até que o usuário clique no botão "OK".

---

## 2. `prompt()` — Captura de Dados do Usuário

Abre uma caixa de diálogo solicitando que o usuário digite um texto:

```javascript
const nomeUsuario = prompt("Por favor, digite o seu nome:");
console.log(`Olá, ${nomeUsuario}!`);
```

- Se o usuário digitar algo e clicar em "OK", o método retorna o texto digitado em formato de **String**.
- Se o usuário clicar em "Cancelar" ou fechar a janela, o método retorna o valor primitivo `null`.

---

## A Armadilha Clássica do `prompt()`: Conversão de Tipos

**O `prompt()` SEMPRE retorna uma String**, mesmo quando o usuário digita apenas números!

Se você tentar somar entradas diretas do prompt:

```javascript
const num1 = prompt("Digite o primeiro número:"); // Usuário digita: 10 -> retorna "10"
const num2 = prompt("Digite o segundo número:"); // Usuário digita: 5  -> retorna "5"

console.log(num1 + num2); // Resultado: "105" (CONCATENAÇÃO DE TEXTO, NÃO SOMA!)
```

### A Solução: Converter a String para Number

Utilize `Number()`, `parseInt()` ou `parseFloat()` para converter os dados antes de fazer operações aritméticas:

```javascript
// Conversão explícita com Number()
const numero1 = Number(prompt("Digite o primeiro número:"));
const numero2 = Number(prompt("Digite o segundo número:"));

const soma = numero1 + numero2;
alert(`A soma matemática correta é: ${soma}`); // Agora soma corretamente: 15!
```

---

## 3. `confirm()` — Pergunta Binária (Sim / Não)

Exibe uma caixa com botões "OK" e "Cancelar", retornando um valor booleano:

```javascript
const desejaContinuar = confirm("Deseja realmente excluir este item?");

if (desejaContinuar) {
  console.log("Item excluído com sucesso.");
} else {
  console.log("Operação cancelada pelo usuário.");
}
```
