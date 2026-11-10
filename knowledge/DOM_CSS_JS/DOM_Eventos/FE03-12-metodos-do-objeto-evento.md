# FE03-12 — Métodos do Objeto Evento

## Métodos Essenciais de Controle de Eventos

Além de propriedades informativas, o objeto `event` disponibiliza métodos cruciais para controlar o comportamento do navegador:

---

## 1. `event.preventDefault()` — O Mais Importante

Cancela o **comportamento padrão nativo** que o navegador executaria automaticamente ao disparar aquele evento.

### Casos de Uso Mais Frequentes:

#### No envio de formulários (`submit`):
Impede que a página recarregue e envie os dados em formato síncrono clássico, permitindo tratar os campos com JavaScript e validações locais:
```javascript
form.addEventListener("submit", (e) => {
  e.preventDefault(); // Impede o reload da página!
  // Validações e envio assíncrono via fetch...
});
```

#### Em links (`<a>`):
Impede a navegação imediata para a URL:
```javascript
link.addEventListener("click", (e) => {
  e.preventDefault(); // Não troca de página
  abrirModal();
});
```

---

## 2. `event.stopPropagation()`

Interrompe a propagação do evento nas fases de borbulhamento (*Bubbling*) ou captura (*Capturing*), evitando que elementos pais também disparem seus próprios ouvintes:

```javascript
botaoFilho.addEventListener("click", (e) => {
  e.stopPropagation();
  console.log("Clique capturado apenas no botão filho.");
});
```

---

## 3. `event.stopImmediatePropagation()`

Além de interromper a subida para os nós ancestrais pais, cancela a execução de quaisquer **outros ouvintes de eventos adicionais registrados sobre o mesmo elemento**.
