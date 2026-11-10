# FE02-56 — Atividade: Trabalhando com Objetos I

## Objetivo da Atividade

Praticar a criação de objetos literais, acesso a propriedades via notação de ponto e colchetes, adição de propriedades dinâmicas e criação de métodos internos com uso do `this`.

---

## Enunciado do Desafio

Crie um objeto chamado `carro` que represente um veículo em um sistema de concessionária:

1. Propriedades iniciais:
   - `marca`: `"Toyota"`
   - `modelo`: `"Corolla"`
   - `ano`: `2024`
   - `cor`: `"Prata"`
   - `ligado`: `false`
   - `velocidadeAtual`: `0`
2. Métodos do objeto:
   - `ligar()`: altera a propriedade `ligado` para `true` e exibe mensagem informativa.
   - `desligar()`: altera `ligado` para `false`, zera a velocidade e exibe aviso.
   - `acelerar(km)`: se o carro estiver ligado, aumenta a `velocidadeAtual` pelo valor informado e exibe a nova velocidade; se estiver desligado, avisa que não é possível acelerar com o carro desligado.
   - `obterDescricao()`: retorna uma string completa formatando marca, modelo, ano, cor e estado atual.

---

## Solução de Referência

```javascript
const carro = {
  marca: "Toyota",
  modelo: "Corolla",
  ano: 2024,
  cor: "Prata",
  ligado: false,
  velocidadeAtual: 0,

  ligar() {
    this.ligado = true;
    console.log(`${this.modelo} foi ligado.`);
  },

  desligar() {
    this.ligado = false;
    this.velocidadeAtual = 0;
    console.log(`${this.modelo} foi desligado e parou totalmente.`);
  },

  acelerar(km) {
    if (!this.ligado) {
      console.log(`Não é possível acelerar: o ${this.modelo} está desligado!`);
      return;
    }
    this.velocidadeAtual += km;
    console.log(`Acelerando! Velocidade atual: ${this.velocidadeAtual} km/h.`);
  },

  obterDescricao() {
    const statusMotor = this.ligado ? "Ligado" : "Desligado";
    return `${this.marca} ${this.modelo} (${this.ano}) - Cor: ${this.cor} | Motor: ${statusMotor} | Velocidade: ${this.velocidadeAtual} km/h`;
  }
};

// Simulação de uso:
console.log(carro.obterDescricao());
carro.acelerar(20); // Bloqueado pois está desligado
carro.ligar();
carro.acelerar(40);
carro.acelerar(30); // Velocidade: 70 km/h
console.log(carro.obterDescricao());
carro.desligar();
```
