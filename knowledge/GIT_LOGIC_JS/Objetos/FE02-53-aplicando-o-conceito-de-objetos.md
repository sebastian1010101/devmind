# FE02-53 — Aplicando o Conceito de Objetos

## Modelagem de Entidades do Mundo Real

Na engenharia de software, objetos servem para encapsular características completas de uma entidade, garantindo que dados relacionados permaneçam unidos sob uma mesma estrutura lógica.

---

## Exemplo de Modelagem: Perfil de Aluno

```javascript
const aluno = {
  matricula: "KZ-2026-09",
  nomeCompleto: "Mariana Costa",
  curso: "Desenvolvimento Web Full Stack",
  moduloAtual: "Módulo 2 - Git e Lógica com JavaScript",
  notas: [9.5, 8.0, 10.0],
  endereco: {
    rua: "Avenida República Argentina",
    numero: 1500,
    cidade: "Curitiba",
    uf: "PR"
  },
  ativo: true
};
```

---

## Acessando Objetos Aninhados (Nested Objects)

Quando um objeto contém outro objeto como propriedade, encadeiam-se os pontos na navegação:

```javascript
// Acessando a cidade do endereço do aluno:
console.log(aluno.endereco.cidade); // "Curitiba"

// Acessando a primeira nota do array de notas:
console.log(aluno.notas[0]); // 9.5
```

---

## Verificando a Existência de Propriedades

Para checar se uma propriedade existe em um objeto antes de tentar usá-la:

```javascript
// 1. Operador 'in':
console.log("matricula" in aluno); // true
console.log("telefone" in aluno);  // false

// 2. Encadeamento Opcional (Optional Chaining - ?. do ES2020):
// Evita que o programa quebre com TypeError caso o objeto intermediário seja null ou undefined:
console.log(aluno.responsavel?.nome); // undefined (sem estourar erro no console!)
```
