# FE02-44 — Depuração e console

## Depuração de Laços com Ferramentas do Desenvolvedor

Quando laços de repetição realizam centenas de iterações, inspecionar manualmente com testes de mesa ou lotar o terminal com milhares de `console.log()` torna-se inviável.

O painel **Sources (Fontes)** nas Ferramentas do Desenvolvedor (*DevTools*) do navegador oferece recursos profissionais para depurar loops.

---

## 1. Pontos de Interrupção (Breakpoints)

Um **breakpoint** instrui o navegador a **pausar a execução do programa exatamente em uma linha específica**.

### Como Utilizar no Navegador:
1. Abra o DevTools (`F12`) &rarr; aba **Sources**.
2. Abra seu arquivo JavaScript.
3. Clique sobre o **número da linha** onde o loop se inicia (ex: na linha do `for` ou dentro dele).
4. Recarregue a página: o código congelará no breakpoint antes de executar aquela linha.

---

## 2. Breakpoints Condicionais (Conditional Breakpoints)

Em um loop que roda 1000 vezes, pausar manualmente em cada volta é exaustivo. O breakpoint condicional permite pausar **apenas quando uma condição específica for atingida**:

1. Clique com o botão direito do mouse sobre o número da linha no painel Sources.
2. Selecione **Add conditional breakpoint...**.
3. Digite a condição desejada (ex: `i === 995` ou `total < 0`).
4. O navegador executará em velocidade máxima as primeiras 994 voltas e só pausará quando a condição for verdadeira.

---

## 3. A Instrução Nativa `debugger;`

Você pode inserir a instrução `debugger;` diretamente no seu arquivo de código-fonte:

```javascript
for (let i = 1; i <= 50; i++) {
  const calculo = i * 3;

  if (calculo === 60) {
    debugger; // O navegador pausa automaticamente aqui se o DevTools estiver aberto!
  }
}
```

Ao atingir essa linha com o painel F12 aberto, o navegador congela o programa e permite inspecionar o valor exato de cada variável em memória no painel lateral de **Scope**.
