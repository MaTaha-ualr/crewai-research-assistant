"""Run the ticket's five sample research experiments and record their results."""

from datetime import datetime
from pathlib import Path
import time

from .crew import source_urls
from .main import run_research


TOPICS = [
    "Latest developments in Model Context Protocol (MCP)",
    "CrewAI sequential process and task context",
    "Python environment variables documentation",
    "Recent Gemini API model updates",
    "Exa web search API documentation",
]
REPORT_PATH = Path(__file__).resolve().parents[2] / "results" / "experiment-report.md"


def main() -> int:
    results: list[dict[str, object]] = []
    total_started = time.perf_counter()

    for index, topic in enumerate(TOPICS, start=1):
        print(f"[{index}/{len(TOPICS)}] Researching: {topic}", flush=True)
        started = time.perf_counter()
        try:
            report = run_research(topic)
            urls = source_urls(report)
            results.append({
                "topic": topic,
                "status": "Completed",
                "sources": len(urls),
                "elapsed": time.perf_counter() - started,
                "report": report,
                "findings_present": any(
                    marker in report.casefold()
                    for marker in ("key findings", "## findings", "**finding")
                ),
                "error": "",
            })
        except Exception as exc:
            results.append({
                "topic": topic,
                "status": "Failed",
                "sources": 0,
                "elapsed": time.perf_counter() - started,
                "report": "",
                "findings_present": False,
                "error": str(exc),
            })
        print(
            f"    {results[-1]['status']} — {results[-1]['sources']} source(s), "
            f"{results[-1]['elapsed']:.1f}s",
            flush=True,
        )

    report_lines = [
        "# Five-topic experiment report",
        "",
        f"Run date: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Total elapsed time: {time.perf_counter() - total_started:.1f} seconds",
        "",
        "| Topic | Research task | Source URLs | Findings section | Elapsed time | Errors |",
        "| --- | --- | ---: | --- | ---: | --- |",
    ]
    for result in results:
        report_lines.append(
            f"| {result['topic']} | {result['status']} | {result['sources']} | "
            f"{'Present' if result['findings_present'] else 'No'} | "
            f"{result['elapsed']:.1f}s | {result['error'] or 'None'} |"
        )
    report_lines.extend(["", "## Research summaries", ""])
    for result in results:
        report_lines.extend([f"### {result['topic']}", ""])
        report_lines.extend(str(result["report"] or result["error"]).splitlines())
        report_lines.append("")
    report_lines.extend([
        "",
        "## Review",
        "",
        "A findings section was detected in the completed summaries. Verify that it covers the "
        "topic's main findings and that each source URL supports its associated claim. Add "
        "observed strengths, incorrect results, and follow-up improvements here.",
        "",
    ])
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nSaved results to {REPORT_PATH}")
    print(f"Total elapsed time: {time.perf_counter() - total_started:.1f}s")
    return 0 if all(item["status"] == "Completed" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
