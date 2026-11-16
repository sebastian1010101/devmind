import Link from "next/link";
export default function Terms() {
  return <main className="legal">
    <Link href="/">← DevMind</Link>
    <h1>Termos de uso</h1>
    <p>Versão de 16 de novembro de 2026. Acesso destinado a pessoas com 18 anos ou mais residentes no Brasil para estudo de conteúdos técnicos públicos.</p>
    <h2>Uso responsável</h2>
    <p>Use sua própria conta. Envie apenas informações técnicas públicas que você tem direito de compartilhar. Proteja suas credenciais e respeite os limites de uso. O serviço não recebe documentos privados nesta fase.</p>
    <h2>Respostas e avaliações</h2>
    <p>A IA pode errar. Confira as fontes, a resposta de referência e as qualificações do documento. A autoavaliação organiza a próxima revisão. O progresso registrado descreve atividades de estudo e depende da avaliação automática.</p>
    <h2>Conta gratuita e disponibilidade</h2>
    <p>Operações de IA têm cotas diárias, limites de solicitações e concorrência. Os provedores podem interromper ou limitar o serviço. Gratuidade e disponibilidade estão sujeitas à configuração do projeto, região e condições dos provedores.</p>
    <h2>Estado do projeto</h2>
    <p>O DevMind está em preparação para uso público. A abertura depende da validação das integrações, do corpus, das condições comerciais e regionais dos provedores e da publicação de um canal de contato e atendimento aos direitos de privacidade.</p>
    <p>
      <Link href="/privacidade">Leia a política de privacidade</Link>
    </p>
  </main>;
}
