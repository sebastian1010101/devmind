# Interface do DevMind

Execute o backend FastAPI conforme o [README principal](../README.md). Depois, neste diretório:

```bash
npm ci
npm run dev
```

Abra [localhost:3035](http://localhost:3035). O frontend usa `http://localhost:8000` por padrão. Para outro endereço, copie `.env.example` para `.env.local` e ajuste `API_URL`. O navegador usa o proxy same-origin `/api`. Configure `API_URL` tanto no build quanto no processo `next start`.

A homepage pública fica em `/`. Crie uma conta e confirme o email para entrar em `/dashboard`. A [entrega multiusuário](../docs/PUBLIC_RELEASE.md) descreve a configuração Supabase e as verificações pendentes.

O chat preserva o histórico durante a sessão da página. Use **Guia** para navegar na base local e selecionar um escopo de consulta. Use `/help` para ver os comandos do terminal e `?debug=true` para exibir similaridade, fragmento e latência.

Verifique com `npm run lint`, `npx tsc --noEmit` e `npm run build -- --webpack`.
