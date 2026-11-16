import Link from "next/link";
export default function Privacy() {
  return <main className="legal">
    <Link href="/">← DevMind</Link>
    <h1>Privacidade</h1>
    <p>Versão de 16 de novembro de 2026. DevMind é um projeto de portfólio para estudo técnico de adultos residentes no Brasil.</p>
    <h2>Dados e finalidade</h2>
    <p>O Supabase Auth processa email, senha e confirmação de conta. O backend armazena seus cartões, respostas, tentativas, avaliações, calendário e sessões para recuperar seu progresso. Cookies HttpOnly mantêm a sessão. Rascunhos de estudo ficam no armazenamento da aba do navegador, separados por conta.</p>
    <h2>Provedores de IA</h2>
    <p>Perguntas técnicas, respostas de estudo e trechos do corpus são enviados ao provedor de geração configurado, Gemini ou OpenAI. O Pinecone processa a consulta para recuperar evidências. Evite dados pessoais, sensíveis, sigilosos e código proprietário. No serviço gratuito Gemini, conteúdo pode ser usado para melhorar produtos e revisado por pessoas. A disponibilidade depende da conta e região.</p>
    <h2>Segurança e retenção</h2>
    <p>O servidor valida a identidade e restringe o acesso ao seu progresso. Registros técnicos guardam consumo, latência e códigos de erro. Limites por IP usam identificadores derivados. Dados de estudo permanecem até a exclusão administrativa da conta e seus registros associados. A política de retenção de backups e um canal de contato do responsável precisam ser definidos antes da abertura pública.</p>
    <p>Consulte os <Link href="/termos">termos de uso</Link>. Esta versão deve ser revisada pelo responsável pelo projeto antes do lançamento público.</p>
  </main>;
}
