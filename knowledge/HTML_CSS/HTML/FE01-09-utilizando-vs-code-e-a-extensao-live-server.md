# FE01-09 — Utilizando VS Code e a Extensão Live Server

## O Problema de Abrir Arquivos Diretamente no Navegador

Ao dar um duplo clique em um arquivo `index.html`, o navegador abre o recurso com o protocolo `file:///home/.../index.html`. 

Limitações do protocolo `file://`:
- Não há atualização automática da página quando o código é alterado e salvo.
- Caminhos absolutos em links e imagens podem quebrar.
- Chamadas assíncronas (como requisições `fetch` e APIs modernas) são bloqueadas por políticas de segurança do navegador.

---

## Como o Live Server Funciona

A extensão **Live Server** cria um servidor web local real na máquina (geralmente sob a porta `5500`, endereço `http://127.0.0.1:5500` ou `http://localhost:5500`).

- Injeta um script leve de escuta de eventos via WebSocket no HTML em execução.
- Sempre que qualquer arquivo do projeto é salvo (`Ctrl + S`), o servidor notifica a página no navegador para recarregar sem necessidade de apertar `F5`.

---

## Como Iniciar e Encerrar o Live Server

### Método 1: Pela Barra de Status Inferior
1. Abra a pasta do projeto no VS Code (`File > Open Folder`).
2. Abra o arquivo `index.html`.
3. Clique no botão **"Go Live"** no canto inferior direito da barra de status do VS Code.
4. Para fechar, clique no mesmo botão (que estará exibindo a porta ativa, ex: `Port: 5500`).

### Método 2: Pelo Menu de Contexto
1. Clique com o botão direito do mouse sobre o arquivo `index.html` ou dentro da área de código.
2. Selecione a opção **"Open with Live Server"**.
3. Para interromper, selecione **"Stop Live Server"**.
