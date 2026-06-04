"""
Benchmark de comparação entre provedores de IA na análise de laudos.

Compara o Google Gemini (ex.: gemini-3.1-flash-lite) com o Amazon Nova Lite
(via Bedrock) sobre os mesmos laudos, avaliando:

  - Tempo de resposta: medido apenas na chamada ao modelo (em ms).
  - Qualidade de extração: concordância campo a campo entre os dois modelos
    (cisto, nódulo, calcificação, microcalcificação e BI-RADS).

Como a comparação é de modelo-vs-modelo (sem gabarito), o relatório mostra a
concordância entre os dois e salva ambas as saídas lado a lado para revisão
manual das divergências.

Uso:
    python compare.py [--runs N] [--exams-dir CAMINHO] [--report ARQUIVO]

Configuração (via .env, veja .env.example):
    GEMINI_API_KEY, GEMINI_MODEL          -> Google Gemini
    AWS_REGION, NOVA_MODEL_ID + creds AWS -> Amazon Nova (Bedrock)
"""
import argparse
import glob
import json
import os
import statistics

from src.ai_client import get_ai_client
from src.config import config


# Campos booleanos de presença comparados para concordância.
PRESENCE_FIELDS = ["cisto", "nodulo", "calcificacao", "microcalcificacao"]


def read_file(path: str) -> str:
    """Lê o conteúdo de um arquivo de texto."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _presence(analysis: dict, field: str):
    """Extrai o booleano de presença de um campo, tolerando estruturas faltantes."""
    value = analysis.get(field)
    if isinstance(value, dict):
        return bool(value.get("presente"))
    return None


def _normalize_birads(analysis: dict) -> str:
    """Normaliza o BI-RADS para comparação (ex.: 'BI-RADS 4C' -> '4')."""
    raw = str(analysis.get("bi_rads", "")).strip().upper()
    digits = "".join(ch for ch in raw if ch.isdigit())
    return digits or raw


def compare_analyses(a: dict, b: dict) -> dict:
    """
    Compara dois resultados de extração e retorna a concordância por campo.

    Args:
        a: Análise do provedor A (Gemini)
        b: Análise do provedor B (Nova)

    Returns:
        Dicionário com a concordância por campo e o total de campos coincidentes.
    """
    fields = {}
    for field in PRESENCE_FIELDS:
        va, vb = _presence(a, field), _presence(b, field)
        fields[field] = {"a": va, "b": vb, "match": va == vb}

    ba, bb = _normalize_birads(a), _normalize_birads(b)
    fields["bi_rads"] = {"a": ba, "b": bb, "match": ba == bb}

    matches = sum(1 for f in fields.values() if f["match"])
    return {"fields": fields, "matches": matches, "total": len(fields)}


def run_model(client, content: str, runs: int):
    """
    Executa o modelo `runs` vezes sobre o mesmo conteúdo.

    Returns:
        Tupla (última_análise, [tempos_em_ms]).
    """
    timings_ms = []
    analysis = None
    for _ in range(runs):
        analysis, elapsed_ns = client.analyze_exam_with_timing(content)
        timings_ms.append(elapsed_ns / 1_000_000)
    return analysis, timings_ms


def _fmt_ms(values) -> str:
    """Formata estatísticas de tempo (média / mediana / min) em ms."""
    if not values:
        return "n/a"
    return (
        f"média {statistics.mean(values):8.1f} ms | "
        f"mediana {statistics.median(values):8.1f} ms | "
        f"min {min(values):8.1f} ms"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Compara Gemini vs Amazon Nova Lite em laudos de mamografia."
    )
    parser.add_argument(
        "--runs", type=int, default=1,
        help="Número de execuções por modelo/laudo para média de tempo (padrão: 1).",
    )
    parser.add_argument(
        "--exams-dir", default=config.exams_directory,
        help="Diretório com os laudos .txt (padrão: config EXAMS_DIR).",
    )
    parser.add_argument(
        "--report", default="comparison_report.json",
        help="Caminho do relatório JSON de saída (padrão: comparison_report.json).",
    )
    args = parser.parse_args()

    exams_dir = args.exams_dir
    text_files = sorted(glob.glob(os.path.join(exams_dir, "*.txt")))
    if not text_files:
        print(f"Nenhum arquivo .txt encontrado em: {exams_dir}")
        return

    print("=" * 70)
    print("COMPARAÇÃO DE MODELOS — Gemini vs Amazon Nova Lite")
    print("=" * 70)
    print(f"Laudos:   {len(text_files)} arquivo(s) em '{exams_dir}'")
    print(f"Execuções por modelo/laudo: {args.runs}")

    # Inicializa os dois provedores explicitamente.
    gemini = get_ai_client("gemini")
    nova = get_ai_client("nova")
    print(f"Gemini:   {gemini.model_name}")
    print(f"Nova:     {nova.model_name} (região {config.aws_region})")
    print("=" * 70)

    results = []
    gemini_timings_all = []
    nova_timings_all = []
    field_match_counts = {f: 0 for f in PRESENCE_FIELDS + ["bi_rads"]}
    field_compared = 0  # laudos onde ambos extraíram com sucesso
    total_matches = 0
    total_fields = 0

    for path in text_files:
        name = os.path.basename(path)
        print(f"\n--- {name} ---")
        content = read_file(path)
        base = os.path.splitext(path)[0]

        entry = {"file": name}

        # Gemini
        try:
            g_analysis, g_timings = run_model(gemini, content, args.runs)
            gemini_timings_all.extend(g_timings)
            entry["gemini"] = {"timings_ms": g_timings, "analysis": g_analysis}
            with open(f"{base}_gemini.json", "w", encoding="utf-8") as f:
                json.dump(g_analysis, f, ensure_ascii=False, indent=4)
            print(f"  Gemini -> {_fmt_ms(g_timings)}")
        except Exception as e:
            g_analysis = None
            entry["gemini"] = {"error": str(e)}
            print(f"  Gemini -> ERRO: {e}")

        # Nova
        try:
            n_analysis, n_timings = run_model(nova, content, args.runs)
            nova_timings_all.extend(n_timings)
            entry["nova"] = {"timings_ms": n_timings, "analysis": n_analysis}
            with open(f"{base}_nova.json", "w", encoding="utf-8") as f:
                json.dump(n_analysis, f, ensure_ascii=False, indent=4)
            print(f"  Nova   -> {_fmt_ms(n_timings)}")
        except Exception as e:
            n_analysis = None
            entry["nova"] = {"error": str(e)}
            print(f"  Nova   -> ERRO: {e}")

        # Concordância (apenas se ambos extraíram)
        if g_analysis is not None and n_analysis is not None:
            cmp = compare_analyses(g_analysis, n_analysis)
            entry["agreement"] = cmp
            field_compared += 1
            total_matches += cmp["matches"]
            total_fields += cmp["total"]
            for field, info in cmp["fields"].items():
                if info["match"]:
                    field_match_counts[field] += 1
            print(f"  Concordância: {cmp['matches']}/{cmp['total']} campos")
            for field, info in cmp["fields"].items():
                flag = "OK " if info["match"] else "DIF"
                print(f"      [{flag}] {field:18s} G={info['a']!s:7s} N={info['b']!s:7s}")

        results.append(entry)

    # ----- Resumo -----
    print("\n" + "=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"Tempo Gemini: {_fmt_ms(gemini_timings_all)}")
    print(f"Tempo Nova:   {_fmt_ms(nova_timings_all)}")

    if gemini_timings_all and nova_timings_all:
        g_med = statistics.median(gemini_timings_all)
        n_med = statistics.median(nova_timings_all)
        faster, slower = ("Nova", "Gemini") if n_med < g_med else ("Gemini", "Nova")
        ratio = max(g_med, n_med) / min(g_med, n_med) if min(g_med, n_med) else 0
        print(f"Mais rápido (mediana): {faster} (~{ratio:.2f}x vs {slower})")

    if field_compared:
        pct = 100.0 * total_matches / total_fields if total_fields else 0
        print(f"\nConcordância geral: {total_matches}/{total_fields} campos "
              f"({pct:.1f}%) em {field_compared} laudo(s)")
        print("Concordância por campo:")
        for field in PRESENCE_FIELDS + ["bi_rads"]:
            c = field_match_counts[field]
            fp = 100.0 * c / field_compared
            print(f"   {field:18s} {c}/{field_compared}  ({fp:.0f}%)")
    else:
        print("\nSem laudos com extração bem-sucedida em ambos os modelos.")

    # Relatório completo em JSON
    summary = {
        "exams_dir": exams_dir,
        "runs_per_model": args.runs,
        "gemini_model": gemini.model_name,
        "nova_model": nova.model_name,
        "aws_region": config.aws_region,
        "timing_ms": {
            "gemini": _timing_stats(gemini_timings_all),
            "nova": _timing_stats(nova_timings_all),
        },
        "agreement": {
            "exams_compared": field_compared,
            "total_matches": total_matches,
            "total_fields": total_fields,
            "by_field": {
                f: {"matches": field_match_counts[f], "of": field_compared}
                for f in PRESENCE_FIELDS + ["bi_rads"]
            },
        },
        "results": results,
    }
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
    print(f"\nRelatório salvo em: {args.report}")
    print("Saídas por laudo salvas como *_gemini.json e *_nova.json")
    print("=" * 70)


def _timing_stats(values) -> dict:
    """Resumo estatístico de uma lista de tempos (ms)."""
    if not values:
        return {}
    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
    }


if __name__ == "__main__":
    main()
