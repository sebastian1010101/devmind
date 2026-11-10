# FE02-11 — Atividade: Praticando Operadores

## Objetivo da Atividade

Aplicar na prática todos os operadores aritméticos (`+`, `-`, `*`, `/`, `%`, `**`), regras de precedência com parênteses e operadores de atribuição abreviada para resolver problemas matemáticos comuns do desenvolvimento web.

---

## Enunciado do Desafio

Escreva um script em JavaScript (`calculos.js`) que resolva as quatro situações abaixo:

1. **Cálculo de Área e Perímetro:**
   - Dado um retângulo de base `12` e altura `8`.
   - Calcule e exiba a área (`base * altura`) e o perímetro (`2 * (base + altura)`).
2. **Conversão de Temperatura:**
   - Converta uma temperatura de `30` graus Celsius para Fahrenheit utilizando a fórmula: `F = (C * 9/5) + 32`.
3. **Cálculo do IMC (Índice de Massa Corporal):**
   - Dados o peso de `75` kg e a altura de `1.75` m.
   - Calcule o IMC utilizando o operador de exponenciação: `peso / (altura ** 2)`.
4. **Verificação de Paridade:**
   - Dado um número inteiro qualquer (ex: `47`).
   - Calcule o resto da divisão por 2 e imprima se o resto é zero.

---

## Solução de Referência

```javascript
// 1. Área e Perímetro do Retângulo
const baseRetangulo = 12;
const alturaRetangulo = 8;
const area = baseRetangulo * alturaRetangulo;
const perimetro = 2 * (baseRetangulo + alturaRetangulo);

console.log("=== 1. RETÂNGULO ===");
console.log("Área:", area);          // 96
console.log("Perímetro:", perimetro); // 40

// 2. Conversão de Temperatura (Celsius para Fahrenheit)
const celsius = 30;
const fahrenheit = (celsius * 9 / 5) + 32;

console.log("\n=== 2. TEMPERATURA ===");
console.log(`${celsius}°C equivalem a ${fahrenheit}°F`); // 86°F

// 3. Índice de Massa Corporal (IMC)
const pesoKg = 75;
const alturaMetros = 1.75;
const imc = pesoKg / (alturaMetros ** 2);

console.log("\n=== 3. IMC ===");
console.log("IMC calculado:", imc.toFixed(2)); // 24.49

// 4. Verificação de Paridade com Módulo
const numero = 47;
const restoDivisao = numero % 2;
const ehPar = restoDivisao === 0;

console.log("\n=== 4. PARIDADE ===");
console.log(`O número ${numero} é par?`, ehPar);
console.log(`Resto da divisão por 2:`, restoDivisao);
```
