# FE01-32 — Margin, Padding e Border

## As Três Propriedades de Espaçamento e Contorno

---

## 1. Margin (Margem Externa)

Cria espaço vazio ao redor do elemento, afastando-o dos elementos vizinhos.

### Sintaxes de Atalho (*Shorthand*):

```css
/* Quatro valores: Cima, Direita, Baixo, Esquerda (Sentido horário) */
margin: 10px 20px 15px 5px;

/* Três valores: Cima, Laterais (Esquerda + Direita), Baixo */
margin: 10px 20px 15px;

/* Dois valores: Vertical (Cima + Baixo), Horizontal (Esquerda + Direita) */
margin: 20px auto; /* 'auto' nas laterais centraliza blocos com largura definida */

/* Um valor: Todas as quatro direções iguais */
margin: 16px;
```

---

## 2. Padding (Preenchimento Interno)

Cria espaço interno entre o conteúdo do elemento e a sua própria borda. O fundo do elemento (`background-color`) se estende por toda a área do padding.

```css
.botao {
  padding: 12px 24px; /* 12px em cima/baixo e 24px nas laterais */
}
```

---

## 3. Border (Borda)

Desenha uma linha ao redor do preenchimento e do conteúdo.

### Sintaxe Shorthand:
```css
border: [largura] [estilo] [cor];
```

```css
.card {
  border: 1px solid #e0e0e0;
}
```

### Estilos Comuns de Borda (`border-style`):
- `solid`: linha contínua sólida.
- `dashed`: linha tracejada.
- `dotted`: linha pontilhada.
- `none`: sem borda.

### Bordas Arredondadas com `border-radius`:
Modifica os cantos retos da caixa:

```css
.card {
  border-radius: 8px; /* Cantos arredondados suaves */
}

.avatar-circular {
  width: 80px;
  height: 80px;
  border-radius: 50%; /* Transforma uma caixa quadrada em círculo perfeito */
}
```
