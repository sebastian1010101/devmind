# FE02-13 — Atividade: Trabalhando com Strings

## Objetivo da Atividade

Consolidar a manipulação prática do tipo String, aplicando concatenação tradicional, interpolação com Template Literals (`${}`), leitura de comprimento via `.length` e métodos essenciais de transformação de texto (`.toUpperCase()`, `.toLowerCase()`, `.trim()`).

---

## Enunciado do Desafio

Crie um script `strings.js` para formatar os dados de inscrição de um participante em um evento de tecnologia:

1. Declare variáveis com os dados crus recebidos:
   - Primeiro nome com espaços acidentais nas pontas: `"   Sebastián   "`.
   - Sobrenome: `"Gomez"`.
   - Cidade natal: `"curitiba"`.
   - Área de atuação: `"DESENVOLVIMENTO WEB FULL STACK"`.
2. Remova os espaços em branco extras do primeiro nome utilizando `.trim()`.
3. Padronize a cidade para ter apenas letras maiúsculas utilizando `.toUpperCase()`.
4. Padronize a área de atuação para letras minúsculas utilizando `.toLowerCase()`.
5. Calcule a quantidade de caracteres do nome completo (somando primeiro nome limpo + espaço + sobrenome).
6. Construa uma mensagem de crachá de identificação de múltiplas linhas utilizando Template Literals formatando todas as informações tratadas.

---

## Solução de Referência

```javascript
// 1. Dados crus recebidos
const primeiroNomeBruto = "   Sebastián   ";
const sobrenome = "Gomez";
const cidadeNatalBruta = "curitiba";
const areaAtuacaoBruta = "DESENVOLVIMENTO WEB FULL STACK";

// 2, 3 e 4. Tratamento com métodos de string
const primeiroNome = primeiroNomeBruto.trim();
const cidade = cidadeNatalBruta.toUpperCase();
const area = areaAtuacaoBruta.toLowerCase();
const nomeCompleto = `${primeiroNome} ${sobrenome}`;

// 5. Cálculo de caracteres
const totalCaracteresNome = nomeCompleto.length;

// 6. Mensagem do crachá formatada com Template Literals
const crachaIdentificacao = `
========================================
       CRACHÁ DE PARTICIPANTE
========================================
Nome Completo : ${nomeCompleto} (${totalCaracteresNome} caracteres)
Cidade / Polo : ${cidade}
Área Técnica  : ${area}
========================================
Status: Credenciamento Confirmado.
`;

console.log(crachaIdentificacao);
```
