# Arquitetura de DevMind

## Ingestão

1. `main.py` verifica o índice configurado. Quando ausente, cria um índice serverless com `llama-text-embed-v2` e `text → chunk_text`.
2. `ingest.py` usa `stats.py` e `chunking.py` para ler arquivos regulares UTF-8 de até 512 KiB e montar os registros em uma passagem. Arquivos vazios aparecem no resumo. Se houver arquivos inválidos ou nenhum fragmento, o comando falha antes de escrever no índice.
3. A fragmentação respeita seções e fences nas divisões naturais, com limite de 4.000 caracteres. Seções longas tentam subseções, parágrafos e linhas. Um trecho sem ponto natural de corte é dividido com sobreposição limitada.
4. Cada registro guarda o caminho relativo, seção, ordinal, texto, módulo e tema disponíveis. O ID deriva da rota e do ordinal. Caminhos distintos que antes tinham a mesma forma normalizada passam a ter IDs distintos.
5. Os lotes têm até 90 registros de texto. O Pinecone gera os embeddings e persiste a metadata. Com `--prune`, o aplicativo lista IDs gerenciados antes da carga, envia todos os lotes e só então remove os IDs obsoletos. Uma interrupção pode deixar uma carga parcial. Reexecutar o mesmo comando converge para o mesmo conjunto de IDs, respeitada a consistência eventual. [Documentação de upsert](https://docs.pinecone.io/guides/data/upsert-data)

## Pergunta

1. FastAPI valida a pergunta e aceita filtros de escopo opcionais. O chat chama o mesmo `answer_question` usado pela CLI e pela avaliação.
2. Pinecone embute a pergunta e retorna hits ordenados. O pipeline aplica o limiar de relevância aos primeiros `top_k`. O limite de contexto conta o JSON serializado das evidências, incluindo IDs e escapes.
3. A pergunta e os trechos são enviados como dados ao modelo. Sem evidência elegível, a resposta de abstensão é local. Com evidência, uma chamada de Chat Completions produz `answer` e `citations` em JSON Schema estrito.
4. O backend aceita uma resposta com citações presentes no mapa de evidências daquela requisição. A seção, o caminho e o trecho saem da metadata do fragmento. Citações repetidas à mesma seção são agrupadas. Uma saída vazia, inconsistente ou truncada vira erro controlado. [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=chat)
5. O chat exibe a resposta, os trechos citados ou a abstensão. Markdown renderizado do modelo tem HTML, imagens e links externos desativados.

`GET /health` verifica o processo local. `GET /stats` conta a base de arquivos e `GET /guide` lista seus módulos, temas e documentos. Esses endpoints não consultam provedores.

## Configuração e limites

As chaves ficam no processo backend. Clientes são criados sob demanda. O OpenAI recebe uma chamada por resposta com evidência e sem reenvio automático; o SDK Pinecone permite uma nova tentativa com espera limitada. Logs de falhas contêm provedor, classe e status, sem corpo externo. A API converte erros de configuração, timeout, cota e resposta inválida em mensagens públicas.

A distinção entre comandos e dados reduz injeção de prompt. A aplicação não oferece ferramentas ao modelo. A presença de uma citação não demonstra que ela sustenta todas as afirmações. O limite de caracteres reduz custo e tamanho, mas a contagem de tokens varia com o idioma e o conteúdo.

## Avaliação

O avaliador mede Hit@1, @3 e @5 nos ranks brutos dos casos com fonte esperada e recuperação concluída, mesmo se a geração falhar. Ele recupera os ranks extras na mesma busca e limita a geração ao top-k configurado. Atribuição mede se cada referência declarada corresponde ao caminho, seção e ordinal de um fragmento enviado ao modelo. A taxa de fonte esperada citada compara também com os rótulos do dataset.

A acurácia de abstensão inclui as decisões corretas de responder e de se abster entre execuções concluídas. O relatório também apresenta o subconjunto de rejeições esperadas. Latências são medianas das execuções concluídas, com amostras por fase. Taxa de erros usa todas as perguntas. Métricas sem casos elegíveis têm valor nulo.
