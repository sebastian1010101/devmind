# FE02-25 — Atividade: Funções com Parâmetros

## Objetivo da Atividade

Praticar a criação de funções utilitárias que recebem múltiplos parâmetros de diferentes tipos de dados (`string`, `number`), realizam cálculos internos e retornam resultados concretos formatados.

---

## Enunciado do Desafio

Crie um script `calculadora.js` contendo três funções parametrizadas:

1. `calcularDesconto(precoOriginal, porcentagemDesconto)`:
   - Recebe o valor do produto e a porcentagem (ex: 200 e 15).
   - Retorna o valor final com o desconto aplicado.
2. `converterMoeda(valorReais, cotacaoDolar)`:
   - Recebe um valor em reais e o valor da cotação do dólar atual.
   - Retorna o valor equivalente em dólares formatado com duas casas decimais.
3. `gerarNomeUsuario(nome, sobrenome, anoNascimento)`:
   - Recebe o primeiro nome, sobrenome e ano de nascimento.
   - Retorna um identificador em minúsculas no padrão: `nome_sobrenome_ano` (ex: `joao_silva_2001`).

---

## Solução de Referência

```javascript
// 1. Função de cálculo de desconto
function calcularDesconto(precoOriginal, porcentagemDesconto) {
  const valorDesconto = (precoOriginal * porcentagemDesconto) / 100;
  return precoOriginal - valorDesconto;
}

// 2. Função de conversão de moeda
function converterMoeda(valorReais, cotacaoDolar) {
  const dolares = valorReais / cotacaoDolar;
  return dolares.toFixed(2);
}

// 3. Função de geração de identificador
function gerarNomeUsuario(nome, sobrenome, anoNascimento) {
  const nomeTratado = nome.trim().toLowerCase();
  const sobrenomeTratado = sobrenome.trim().toLowerCase();
  return `${nomeTratado}_${sobrenomeTratado}_${anoNascimento}`;
}

// Testes práticos:
console.log("Preço com desconto: R$", calcularDesconto(250, 20)); // R$ 200
console.log("Valor em Dólares: US$", converterMoeda(1000, 5.20));  // US$ 192.31
console.log("Username gerado:", gerarNomeUsuario("Sebastián", "Gomez", 1998)); // sebastián_gomez_1998
```
