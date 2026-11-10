# FE02-32 — Métodos dos Tipos Primitivos

## Objetos Embaladores (Wrapper Objects)

No JavaScript, tipos primitivos como `string` e `number` não são objetos por natureza. No entanto, quando você tenta acessar uma propriedade ou método neles (como `"texto".toUpperCase()`), o motor do JavaScript cria temporariamente um **objeto embalador em memória** (*Wrapper Object*), executa o método e descarta o objeto em seguida.

Isso nos permite utilizar uma rica coleção de métodos utilitários nativos diretamente sobre variáveis primitivas.

---

## Métodos Nativos de String

| Método | Finalidade | Exemplo | Retorno |
| --- | --- | --- | --- |
| `.toUpperCase()` | Converte para maiúsculas | `"dev".toUpperCase()` | `"DEV"` |
| `.toLowerCase()` | Converte para minúsculas | `"DEV".toLowerCase()` | `"dev"` |
| `.trim()` | Remove espaços das extremidades | `"  ola  ".trim()` | `"ola"` |
| `.includes(termo)` | Verifica se contém o termo | `"JavaScript".includes("Script")` | `true` |
| `.replace(antigo, novo)` | Substitui a primeira ocorrência | `"Gato".replace("G", "R")` | `"Rato"` |
| `.replaceAll(antigo, novo)` | Substitui todas as ocorrências | `"a-b-c".replaceAll("-", ".")` | `"a.b.c"` |
| `.slice(inicio, fim)` | Extrai um pedaço do texto | `"Frontend".slice(0, 5)` | `"Front"` |
| `.split(separador)` | Divide a string em um Array | `"maçã,banana".split(",")` | `["maçã", "banana"]` |

---

## Métodos Nativos de Number

| Método | Finalidade | Exemplo | Retorno |
| --- | --- | --- | --- |
| `.toFixed(casas)` | Formata casas decimais (retorna String) | `(10.5678).toFixed(2)` | `"10.57"` |
| `.toString()` | Converte o número para String | `(42).toString()` | `"42"` |
| `Number.parseInt()` | Converte string para número inteiro | `Number.parseInt("15px")` | `15` |
| `Number.parseFloat()` | Converte string para número decimal | `Number.parseFloat("10.5")` | `10.5` |
| `Number.isNaN()` | Verifica se o valor é `NaN` | `Number.isNaN(NaN)` | `true` |
