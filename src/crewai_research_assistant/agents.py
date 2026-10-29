"""Local Ollama model configuration for the research agents."""

import os

from crewai import Agent, LLM


def create_llm() -> LLM:
    """Create the configured local Ollama LLM."""
    return LLM(
        model=os.getenv("MODEL", "ollama/qwen3.5:4b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )


def create_researcher(config: dict, llm: LLM, search_tool) -> Agent:
    """Build the research agent from the CrewAI project YAML config."""
    return Agent(config=config, llm=llm, tools=[search_tool], verbose=True)


def create_summarizer(config: dict, llm: LLM) -> Agent:
    """Build the summarization agent from the CrewAI project YAML config."""
    return Agent(config=config, llm=llm, verbose=True)
