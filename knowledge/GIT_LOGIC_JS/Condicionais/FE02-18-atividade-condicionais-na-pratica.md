# FE02-18 — Atividade: Condicionais na Prática

## Objetivo da Atividade

Praticar o encadeamento de estruturas condicionais (`if`, `else if`, `else`), operadores de comparação estrita (`===`, `>=`, `<=`) e operadores lógicos combinados (`&&`, `||`) para modelar regras de negócio reais.

---

## Enunciado do Desafio 1: Sistema de Classificação de Clientes

Crie um script que receba o total de compras acumuladas de um cliente no ano e defina sua categoria de fidelidade:

- Menor que R$ 500: Categoria **Bronze** (sem frete grátis).
- De R$ 500 até R$ 1.499,99: Categoria **Prata** (5% de cashback).
- De R$ 1.500 até R$ 2.999,99: Categoria **Ouro** (10% de cashback e frete grátis).
- A partir de R$ 3.000: Categoria **Diamante** (15% de cashback, frete grátis e atendimento VIP).

---

## Enunciado do Desafio 2: Validação de Acesso a Evento Noturno

Crie uma verificação de portaria para entrada em uma casa de shows:

- Para entrar, a pessoa deve ter **pelo menos 18 anos**.
- Caso tenha 16 ou 17 anos, só poderá entrar se estiver acompanhada dos pais (`comResponsavel === true`).
- Menores de 16 anos não entram sob hipótese alguma.
- Além da idade, a pessoa deve possuir ingresso válido (`temIngresso === true`).

---

## Solução de Referência

```javascript
// ==========================================
// DESAFIO 1: CLASSIFICAÇÃO DE FIDELIDADE
// ==========================================
const totalComprasAno = 1850.00;
let categoriaCliente = "";
let beneficio = "";

if (totalComprasAno >= 3000) {
  categoriaCliente = "Diamante";
  beneficio = "15% de cashback, frete grátis e atendimento VIP";
} else if (totalComprasAno >= 1500) {
  categoriaCliente = "Ouro";
  beneficio = "10% de cashback e frete grátis";
} else if (totalComprasAno >= 500) {
  categoriaCliente = "Prata";
  beneficio = "5% de cashback";
} else {
  categoriaCliente = "Bronze";
  beneficio = "Sem benefícios adicionais no momento";
}

console.log("=== SISTEMA DE FIDELIDADE ===");
console.log(`Total acumulado: R$ ${totalComprasAno.toFixed(2)}`);
console.log(`Categoria: ${categoriaCliente}`);
console.log(`Benefícios: ${beneficio}`);

// ==========================================
// DESAFIO 2: VALIDAÇÃO DE ACESSO AO EVENTO
// ==========================================
const idadePessoa = 17;
const comResponsavel = true;
const temIngresso = true;

console.log("\n=== PORTARIA DO EVENTO ===");

if (!temIngresso) {
  console.log("Entrada Negada: ingresso não apresentado ou inválido.");
} else if (idadePessoa >= 18) {
  console.log("Entrada Autorizada: maior de idade com ingresso válido.");
} else if (idadePessoa >= 16 && comResponsavel) {
  console.log("Entrada Autorizada: menor acompanhado por responsável legal.");
} else {
  console.log("Entrada Negada: faixa etária não permitida para o evento.");
}
```
