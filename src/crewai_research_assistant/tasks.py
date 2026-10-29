"""Task factories used by the CrewAI project entry point."""

from crewai import Agent, Task


def create_research_task(config: dict, researcher: Agent) -> Task:
    return Task(config=config, agent=researcher)


def create_summary_task(config: dict, summarizer: Agent, research_task: Task) -> Task:
    return Task(
        config=config,
        agent=summarizer,
        context=[research_task],
        markdown=True,
    )
