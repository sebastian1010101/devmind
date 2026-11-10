# FE02-33 — Atividade: Utilizando Métodos

## Objetivo da Atividade

Praticar métodos nativos de String e Number para formatar e tratar dados inseridos de forma imperfeita por usuários em formulários web.

---

## Enunciado do Desafio

Construa um módulo `sanitizacao.js` contendo três funções de tratamento de dados:

1. `formatarNome(nomeCompleto)`:
   - Remove espaços em branco das pontas com `.trim()`.
   - Converte todo o nome para minúsculo e em seguida transforma a primeira letra em maiúscula.
2. `mascararTelefone(telefone)`:
   - Dado um telefone no formato `"41999887766"`.
   - Substitua os dígitos centrais por asteriscos para privacidade, deixando visíveis apenas o DDD e os 4 dígitos finais: `"(41) *****-7766"`.
3. `formatarMoedaReal(valorNumerico)`:
   - Recebe um número float (ex: `1250.5`).
   - Retorna o valor monetário formatado no padrão brasileiro: `"R$ 1250,50"`.

---

## Solução de Referência

```javascript
// 1. Formatar nome próprio
function formatarNome(nomeCompleto) {
  const limpo = nomeCompleto.trim().toLowerCase();
  const primeiraLetraMaiuscula = limpo[0].toUpperCase();
  const restanteNome = limpo.slice(1);

  return primeiraLetraMaiuscula + restanteNome;
}

// 2. Mascarar telefone celular
function mascararTelefone(telefone) {
  const ddd = telefone.slice(0, 2);
  const ultimosDigitos = telefone.slice(-4);

  return `(${ddd}) *****-${ultimosDigitos}`;
}

// 3. Formatação monetária brasileira
function formatarMoedaReal(valorNumerico) {
  const valorComDuasCasas = valorNumerico.toFixed(2);
  const valorComVirgula = valorComDuasCasas.replace(".", ",");

  return `R$ ${valorComVirgula}`;
}

// Testes:
console.log("Nome tratado:", formatarNome("   sEBASTIÁN   ")); // "Sebastián"
console.log("Telefone mascarado:", mascararTelefone("41998881234")); // "(41) *****-1234"
console.log("Valor em Reais:", formatarMoedaReal(3490.9)); // "R$ 3490,90"
```
