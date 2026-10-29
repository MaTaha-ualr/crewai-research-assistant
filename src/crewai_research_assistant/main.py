"""AMP entry points and command-line interface for the research assistant."""

import argparse
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from .crew import ResearchAssistant, create_crew, source_urls


def kickoff(inputs: dict | None = None) -> str:
    """Run the crew with a topic and current-date inputs."""
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    values = dict(inputs or {})
    topic = str(values.get("topic", "")).strip()
    if not topic:
        raise ValueError("Please enter a non-empty research topic.")

    today = date.today()
    values.update(
        topic=topic,
        current_date=today.isoformat(),
        current_year=today.year,
    )
    try:
        result = ResearchAssistant().crew().kickoff(inputs=values)
    except Exception as exc:
        raise RuntimeError(
            "Research failed. Check that Ollama is reachable with the selected model "
            "and that EXA_API_KEY is valid, then try again."
        ) from exc

    report = str(result.raw).strip()
    if not report:
        raise RuntimeError("The crew returned an empty report. Please try again.")
    if not source_urls(report):
        raise RuntimeError(
            "The summary did not include any source URLs. The research may be "
            "insufficient; try a more specific topic."
        )
    return report


def run() -> str:
    """CrewAI project script entry point used by AMP and `crewai run`."""
    topic = os.getenv("RESEARCH_TOPIC", "Latest developments in Model Context Protocol (MCP)")
    return kickoff({"topic": topic})


def run_with_trigger() -> str:
    """CrewAI trigger entry point; reads a JSON payload from the first argument."""
    if len(sys.argv) < 2:
        raise ValueError("Pass a JSON trigger payload containing a topic.")
    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as exc:
        raise ValueError("The trigger payload must be valid JSON.") from exc
    inputs = payload.get("inputs", payload)
    return kickoff(inputs)


def run_research(topic: str) -> str:
    """Compatibility helper used by the five-topic experiment runner."""
    cleaned_topic = topic.strip()
    if not cleaned_topic:
        raise ValueError("Please enter a non-empty research topic.")

    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    crew, summary_task = create_crew()
    today = date.today()
    try:
        result = crew.kickoff(
            inputs={
                "topic": cleaned_topic,
                "current_date": today.isoformat(),
                "current_year": today.year,
            }
        )
    except Exception as exc:
        raise RuntimeError(
            "Research failed. Check that Ollama is reachable with the selected model "
            "and that EXA_API_KEY is valid, then try again."
        ) from exc

    report = str(summary_task.output.raw if summary_task.output else result.raw).strip()
    if not report:
        raise RuntimeError("The crew returned an empty report. Please try again.")
    if not source_urls(report):
        raise RuntimeError(
            "The summary did not include any source URLs. The research may be "
            "insufficient; try a more specific topic."
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Research a topic and summarize sources.")
    parser.add_argument("topic", nargs="*", help="Topic to research")
    args = parser.parse_args()
    topic = " ".join(args.topic) if args.topic else input("Research topic: ")

    started_at = time.perf_counter()
    try:
        report = run_research(topic)
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("\n" + report)
    print(f"\nSources found: {len(source_urls(report))}")
    print(f"Elapsed time: {time.perf_counter() - started_at:.1f} seconds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


if __name__ == "__main__":
    raise SystemExit(main())
