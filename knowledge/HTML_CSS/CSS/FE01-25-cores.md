# FE01-25 — Cores

## Formatos de Representação de Cores no CSS

O CSS suporta diferentes modelos para declarar cores na interface gráfica:

---

## 1. Nomes Nomeados (Named Colors)

O padrão CSS define 140 nomes de cores predefinidos em inglês:

```css
h1 {
  color: red;
  background-color: lightgray;
}
```

- Uso recomendado apenas para testes rápidos e rascunhos.

---

## 2. Código Hexadecimal (HEX)

O formato mais popular na web. Utiliza o caractere `#` seguido de seis dígitos hexadecimais (`0-9` e `A-F`) representando os canais **R**ed, **G**reen e **B**lue (`#RRGGBB`):

```css
p {
  color: #ff5733;        /* Laranja vibrante */
  background: #ffffff;   /* Branco absoluto */
}
```

- **Sintaxe reduzida:** quando os pares são duplicados, podem ser abreviados com três caracteres: `#ffffff` vira `#fff`; `#000000` vira `#000`.
- **Transparência (Alpha):** suporta dois dígitos adicionais no final (`#RRGGBBAA`), ex: `#00000080` (preto com 50% de transparência).

---

## 3. Modelo RGB e RGBA

Define a intensidade de luz Vermelha, Verde e Azul de 0 a 255. O canal **Alpha** (transparência) varia de `0` (totalmente transparente) a `1` (totalmente opaco):

```css
.card {
  /* Sintaxe moderna unificada */
  background-color: rgb(0 112 243 / 0.85);

  /* Sintaxe tradicional compatível */
  background-color: rgba(0, 112, 243, 0.85);
}
```

---

## 4. Modelo HSL e HSLA

Baseado na percepção humana da cor:
- **Hue (Matiz):** ângulo no círculo cromático de 0 a 360 graus (0 = vermelho, 120 = verde, 240 = azul).
- **Saturation (Saturação):** porcentagem de 0% (cinza neutro) a 100% (cor pura).
- **Lightness (Luminosidade):** porcentagem de 0% (preto) a 100% (branco).

```css
.alerta {
  background-color: hsl(0, 100%, 50%);       /* Vermelho puro */
  color: hsl(0, 0%, 100%);                   /* Branco */
}
```

---

## Propriedades CSS Comuns de Cor

- `color`: cor do texto e dos ícones.
- `background-color`: cor de preenchimento de fundo do elemento.
- `border-color`: cor das linhas de borda.
