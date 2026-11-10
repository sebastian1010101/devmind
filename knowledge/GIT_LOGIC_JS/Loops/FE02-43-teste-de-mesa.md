# FE02-43 — Teste de Mesa

## O que é um Teste de Mesa (Trace Table)?

Um **Teste de Mesa** é uma técnica manual de depuração em que o desenvolvedor atua como o próprio motor do computador, acompanhando a execução do algoritmo linha por linha e anotando em uma tabela os valores que cada variável assume a cada momento.

É a forma mais eficaz e rigorosa de entender o funcionamento interno de loops e estruturas condicionais sem adivinhações.

---

## Estrutura da Tabela de Rastreamento

Para construir um teste de mesa:
1. Liste cada variável envolvida em uma coluna.
2. Adicione uma coluna para a **Condição do Loop** avaliada.
3. Adicione uma coluna para a **Saída gerada no Console**.
4. Cada linha da tabela corresponde a uma iteração completa do algoritmo.

---

## Exemplo Prático de Teste de Mesa

Dado o código JavaScript:

```javascript
let soma = 0;

for (let i = 1; i <= 4; i++) {
  soma += i * 2;
  console.log(soma);
}
```

### Tabela de Rastreamento Passo a Passo

| Linha / Momento | Variável `i` | Condição `i <= 4` | Cálculo `soma += i * 2` | Variável `soma` | Saída no Console |
| --- | --- | --- | --- | --- | --- |
| Início | - | - | - | `0` | - |
| 1ª Volta | `1` | `1 <= 4` (`true`) | `0 + (1 * 2)` | `2` | `2` |
| 2ª Volta | `2` | `2 <= 4` (`true`) | `2 + (2 * 2)` | `6` | `6` |
| 3ª Volta | `3` | `3 <= 4` (`true`) | `6 + (3 * 2)` | `12` | `12` |
| 4ª Volta | `4` | `4 <= 4` (`true`) | `12 + (4 * 2)` | `20` | `20` |
| Encerramento | `5` | `5 <= 4` (`false`) | Não executa | `20` | Loop encerrado |

---

## Benefícios do Teste de Mesa

- Permite encontrar **erros de lógica por um** (*off-by-one errors*, ex: usar `<` em vez de `<=`).
- Ajuda a validar se o laço encerra exatamente no ponto esperado.
- Desenvolve a capacidade mental de simular mentalmente o fluxo de execução antes de rodar o código.
