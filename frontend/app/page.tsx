import Image from "next/image";
import Link from "next/link";
const questions = [
  ["Como a IA encontra as respostas?", "O DevMind recupera trechos do catálogo de documentos e usa essas evidências para responder. Você pode abrir as fontes e conferir o contexto. Quando falta evidência, o assistente sinaliza a limitação."],
  ["O que são flashcards inteligentes?", "São perguntas geradas a partir dos documentos. Você responde com suas palavras, recebe feedback da IA e confere a resposta de referência com as fontes utilizadas."],
  ["Como funcionam as revisões?", "Depois de responder, você informa como foi recordar. O calendário usa essa autoavaliação para definir a próxima revisão. Seu painel reúne os cartões pendentes e o progresso por tema."],
  ["Preciso pagar para começar?", "A conta é gratuita. As operações de IA têm limites diários e dependem da disponibilidade dos provedores. Os limites aparecem no painel de estudo."],
  ["Posso enviar informações pessoais?", "Use apenas conteúdo técnico público. Perguntas e respostas de estudo são enviadas ao provedor de IA. Consulte os termos e a política de privacidade antes de criar sua conta. O acesso é destinado a maiores de 18 anos."],
];
export default function Home() {
  return <div className="landing">
    <a className="skip-link" href="#conteudo">Pular para o conteúdo</a>
    <header className="landing-nav wrap">
      <Link href="/" className="brand" aria-label="DevMind, início">
        <span className="brand-mark" aria-hidden="true">&gt;_</span>DevMind</Link>
      <nav aria-label="Navegação principal" className="nav-links">
        <a href="#funcionalidades">Funcionalidades</a>
        <a href="#como-funciona">Como funciona</a>
        <a href="#perguntas">Perguntas</a>
      </nav>
      <div className="nav-actions">
        <Link href="/entrar">Entrar</Link>
        <Link className="button button-small" href="/cadastro">Criar conta <span aria-hidden="true">↗︎</span>
        </Link>
      </div>
    </header>
    <main id="conteudo">
      <section className="hero wrap">
        <p className="eyebrow">SEU PRÓXIMO CONCEITO COMEÇA AQUI</p>
        <h1>Aprenda de verdade<br />com <span>inteligência artificial.</span>
        </h1>
        <p className="hero-description">Estude conteúdos técnicos, tire dúvidas com fontes confiáveis e fortaleça seu conhecimento com revisões inteligentes.</p>
        <div className="hero-actions">
          <Link className="button" href="/cadastro">Começar gratuitamente <span aria-hidden="true">↗︎</span>
          </Link>
          <a className="button button-secondary" href="#como-funciona">Ver como funciona <span aria-hidden="true">↓</span>
          </a>
        </div>
        <p className="hero-note">Respostas com fontes. Prática com propósito. Progresso que fica com você.</p>
        <figure className="app-preview">
          <div className="preview-bar">
            <span className="preview-dots" aria-hidden="true">● ● ●</span>
            <span>devmind / estudo</span>
            <span>Active Recall</span>
          </div>
          <Image src="/previews/study-multiuser.png" width={1440} height={1000} alt="Tela real do DevMind com painel de revisões, seleção de documentos e geração de cartões" priority sizes="(max-width: 900px) 100vw, 1000px" />
          <figcaption>Uma visão da interface de estudo. Captura da versão local.</figcaption>
        </figure>
      </section>
      <section id="funcionalidades" className="features wrap section-space">
        <div className="section-heading">
          <p className="eyebrow">DO ENTENDIMENTO À RECORDAÇÃO</p>
          <h2>Conhecimento que você<br />consegue colocar em prática.</h2>
          <p>Leia, pergunte e teste o que aprendeu. Tudo no mesmo lugar.</p>
        </div>
        <div className="feature-grid">
          <article className="feature-card feature-wide">
            <div>
              <span className="feature-symbol" aria-hidden="true">↳</span>
              <h3>Uma resposta. Fontes para conferir.</h3>
              <p>O chat conecta sua dúvida aos documentos usando RAG. Cada resposta fundamentada traz os trechos e as referências para você ir além da explicação.</p>
              <Link href="/cadastro" className="text-link">Explore o conhecimento <span aria-hidden="true">↗︎</span>
              </Link>
            </div>
            <div className="source-example">
              <span className="mini-label">GIT · EVIDÊNCIA DOCUMENTAL</span>
              <p>Como retirar um arquivo do staging?</p>
              <code>git restore --staged README.md</code>
              <div className="source-reference">↳ Guias DevMind / Git<br />
                <span>Confira a seção e o trecho na resposta.</span>
              </div>
            </div>
          </article>
          <article className="feature-card">
            <span className="feature-symbol" aria-hidden="true">▤</span>
            <h3>Troque a releitura pela prática.</h3>
            <p>Transforme documentos em flashcards inteligentes. Responda com suas palavras e receba feedback com evidências para entender o que precisa revisar.</p>
            <div className="feature-bottom">Pergunta → Sua resposta → Feedback</div>
          </article>
          <article className="feature-card">
            <span className="feature-symbol" aria-hidden="true">↻</span>
            <h3>Volte ao conteúdo no seu ritmo.</h3>
            <p>A repetição espaçada organiza o próximo encontro com cada conceito. Sua percepção de recordação define o calendário e fica salva na sua conta.</p>
            <div className="review-example">
              <span>Hoje</span>
              <i />
              <span>Revisar</span>
              <i />
              <span>Recordar</span>
            </div>
          </article>
        </div>
      </section>
      <section id="como-funciona" className="how-section section-space">
        <div className="wrap">
          <div className="section-heading">
            <p className="eyebrow">UM HÁBITO, TRÊS PASSOS</p>
            <h2>Seu estudo ganha direção.</h2>
          </div>
          <div className="steps">
            <article>
              <h3>Escolha o que aprender</h3>
              <p>Navegue pelo Guia e encontre um módulo, tema ou documento do catálogo técnico.</p>
            </article>
            <article>
              <h3>Entenda e teste seu conhecimento</h3>
              <p>Tire dúvidas com fontes ou gere cartões. Tente responder antes de conferir a referência.</p>
            </article>
            <article>
              <h3>Revise e acompanhe sua evolução</h3>
              <p>Avalie sua recordação, retome os cartões pendentes e acompanhe o progresso por tema.</p>
            </article>
          </div>
        </div>
      </section>
      <section id="perguntas" className="faq wrap section-space">
        <div>
          <p className="eyebrow">AINDA TEM DÚVIDAS?</p>
          <h2>Vamos esclarecer.</h2>
          <p>Conheça a experiência antes<br />de começar a estudar.</p>
        </div>
        <div>{questions.map(([question, answer]) => <details key={question}>
          <summary>{question}<span aria-hidden="true">+</span>
          </summary>
          <p>{answer}</p>
        </details>)}</div>
      </section>
      <section className="closing wrap">
        <p className="eyebrow">MENOS CONTEÚDO ESQUECIDO</p>
        <h2>Dê o próximo passo<br />no seu aprendizado.</h2>
        <Link className="button" href="/cadastro">Começar gratuitamente <span aria-hidden="true">↗︎</span>
        </Link>
      </section>
    </main>
    <footer className="landing-footer wrap">
      <Link href="/" className="brand">
        <span className="brand-mark" aria-hidden="true">&gt;_</span>DevMind</Link>
      <p>Aprender. Recordar. Evoluir.</p>
      <nav aria-label="Informações legais">
        <Link href="/privacidade">Privacidade</Link>
        <Link href="/termos">Termos de uso</Link>
      </nav>
    </footer>
  </div>;
}
