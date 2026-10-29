"""OpenAI model configuration for the research agents."""

import os

from crewai import Agent, LLM


def create_llm() -> LLM:
    """Create the configured OpenAI LLM without hardcoding a model in code."""
    return LLM(
        model=os.getenv("MODEL", "gpt-6-luna"),
        api_key=os.getenv("OPENAI_API_KEY"),
        reasoning_effort="none",
    )


def create_researcher(config: dict, llm: LLM, search_tool) -> Agent:
    """Build the research agent from the CrewAI project YAML config."""
    return Agent(config=config, llm=llm, tools=[search_tool], verbose=True)


def create_summarizer(config: dict, llm: LLM) -> Agent:
    """Build the summarization agent from the CrewAI project YAML config."""
    return Agent(config=config, llm=llm, verbose=True)
