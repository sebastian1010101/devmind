# FE02-19 — Atividade: Condicionais com TAF

## O que é um TAF?

O **Teste de Aptidão Física (TAF)** é uma avaliação prática comum em concursos públicos (como Polícia Militar, Bombeiros e Forças Armadas) para certificar se os candidatos atingiram os índices físicos mínimos de resistência e força exigidos pelo cargo.

---

## Enunciado do Desafio

Construa um algoritmo em JavaScript (`taf.js`) para avaliar se um candidato foi aprovado ou reprovado no TAF militar, considerando critérios diferentes para candidatos do sexo masculino e feminino:

### Critérios de Avaliação

1. **Candidatos Masculinos (`sexo === "M"`):**
   - Flexões de braço na barra fixa: no mínimo `6 repetições`.
   - Abdominais: no mínimo `35 repetições` em 1 minuto.
   - Corrida de 12 minutos: distância mínima de `2400 metros`.
2. **Candidatas Femininas (`sexo === "F"`):**
   - Flexões de braço na barra fixa: no mínimo `15 segundos de sustentação isométrica`.
   - Abdominais: no mínimo `30 repetições` em 1 minuto.
   - Corrida de 12 minutos: distância mínima de `2000 metros`.

O candidato só é considerado **APROVADO** se atingir ou superar as marcas mínimas em **todas as três provas simultaneamente**. Se falhar em qualquer uma delas, o resultado é **REPROVADO**.

---

## Solução de Referência

```javascript
// Dados de teste do candidato:
const nomeCandidato = "Carlos Eduardo";
const sexo = "M"; // "M" ou "F"
const repeticoesBarra = 7;     // Masculino: repetições | Feminino: segundos sustentados
const repeticoesAbdominais = 38;
const metrosCorrida = 2450;

let passouBarra = false;
let passouAbdominal = false;
let passouCorrida = false;

// 1. Avaliação conforme o sexo biológico regulamentar
if (sexo === "M") {
  passouBarra = repeticoesBarra >= 6;
  passouAbdominal = repeticoesAbdominais >= 35;
  passouCorrida = metrosCorrida >= 2400;
} else if (sexo === "F") {
  passouBarra = repeticoesBarra >= 15;
  passouAbdominal = repeticoesAbdominais >= 30;
  passouCorrida = metrosCorrida >= 2000;
} else {
  console.log("Erro: gênero não reconhecido no regulamento.");
}

// 2. Determinação do veredito final
const aprovadoNoTAF = passouBarra && passouAbdominal && passouCorrida;

console.log("========================================");
console.log(`RELATÓRIO TAF — CANDIDATO: ${nomeCandidato}`);
console.log("========================================");
console.log(`Barra Fixa  : ${passouBarra ? "APROVADO" : "REPROVADO"}`);
console.log(`Abdominais  : ${passouAbdominal ? "APROVADO" : "REPROVADO"}`);
console.log(`Corrida     : ${passouCorrida ? "APROVADO" : "REPROVADO"}`);
console.log("----------------------------------------");
console.log(`RESULTADO FINAL: ${aprovadoNoTAF ? "APROVADO NO CONCURSO!" : "REPROVADO NO TAF"}`);
console.log("========================================");
```
