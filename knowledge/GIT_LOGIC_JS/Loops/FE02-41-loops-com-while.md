# FE02-41 — Loops com while

## A Estrutura do Laço `while`

O comando `while` ("enquanto") é a estrutura de repetição mais flexível do JavaScript. Ele avalia uma condição booleana **antes de cada volta**: enquanto a condição for avaliada como `true`, o bloco interno de código continua sendo executado.

```javascript
while (condicao) {
  // Código executado repetidamente
}
```

---

## Quando Usar `while` vs `for`?

- **Use `for`:** quando a quantidade de repetições é previsível ou controlada por um índice numérico direto (ex: de 1 a 10).
- **Use `while`:** quando você **não sabe previamente quantas voltas serão necessárias**, pois a condição de parada depende de um evento externo (ex: o usuário digitar uma senha correta, um número aleatório ser sorteado ou uma resposta de rede chegar).

---

## Exemplo 1: Contador Básico Controlado

```javascript
let contador = 1;

while (contador <= 5) {
  console.log(`Contagem atual: ${contador}`);
  contador++; // OBRIGATÓRIO: garante que o contador atinja a condição de parada
}
```

---

## Exemplo 2: Repetição Baseada em Evento

```javascript
// Simulação de tentativas de conexão de rede
let conectado = false;
let tentativas = 0;

while (!conectado && tentativas < 3) {
  tentativas++;
  console.log(`Tentativa ${tentativas} de conexão ao servidor...`);

  if (tentativas === 2) {
    conectado = true; // Simula sucesso na segunda tentativa
  }
}

if (conectado) {
  console.log("Conexão estabelecida com sucesso!");
} else {
  console.log("Falha ao conectar após 3 tentativas.");
}
```

---

## A Variação `do...while`

Enquanto o `while` testa a condição no início (podendo executar zero vezes se a condição for falsa de partida), o `do...while` testa a condição **no final**, garantindo que o bloco seja executado **pelo menos uma vez obrigatoriamente**:

```javascript
let opcao = 0;

do {
  console.log("Menu principal exibido.");
  // Garante a primeira exibição mesmo se opcao já for 0
} while (opcao !== 0);
```
