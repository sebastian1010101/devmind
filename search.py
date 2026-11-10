"""CLI de busca. Use --debug para inspecionar os resultados da mesma busca."""

import argparse

from pydantic import ValidationError

from providers import ServiceError
from rag import RunTrace, answer_question, format_debug_hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Pergunte à base de conhecimento do DevMind.")
    parser.add_argument("--top-k", type=int)
    parser.add_argument("--debug", action="store_true", help="Mostra os resultados da recuperação e os tempos.")
    args = parser.parse_args()
    trace = RunTrace()
    try:
        result = answer_question(input("Pergunta: "), top_k=args.top_k, trace=trace)
    except (EOFError, ValidationError):
        parser.error("Informe uma pergunta de 1 a 1200 caracteres e top-k de 1 a 20.")
    except ServiceError as exc:
        print(exc)
        return 1

    print(f"\n{result['answer']}")
    for item in result["sources"]:
        print(f"- {item['source']} · {item['section']}")
    if args.debug:
        print(f"\nTempo total: {trace.total_ms:.1f} ms")
        print(format_debug_hits(trace.hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
