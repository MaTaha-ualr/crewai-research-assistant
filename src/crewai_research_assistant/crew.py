"""AMP-compatible CrewAI crew and report validation helpers."""

import re

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from crewai_research_assistant.agents import (
    create_llm,
    create_researcher,
    create_summarizer,
)
from crewai_research_assistant.tasks import create_research_task, create_summary_task
from crewai_research_assistant.tools import create_search_tool


SOURCE_URL_PATTERN = re.compile(r"https?://[^\s)\]>]+", re.IGNORECASE)


@CrewBase
class ResearchAssistant:
    """Two-agent sequential crew in CrewAI's classic AMP project format."""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def researcher(self) -> Agent:
        return create_researcher(
            self.agents_config["researcher"],  # type: ignore[index]
            create_llm(),
            create_search_tool(),
        )

    @agent
    def summarizer(self) -> Agent:
        return create_summarizer(
            self.agents_config["summarizer"],  # type: ignore[index]
            create_llm(),
        )

    @task
    def research_task(self) -> Task:
        return create_research_task(
            self.tasks_config["research_task"],  # type: ignore[index]
            self.researcher(),
        )

    @task
    def summary_task(self) -> Task:
        return create_summary_task(
            self.tasks_config["summary_task"],  # type: ignore[index]
            self.summarizer(),
            self.research_task(),
        )

    @crew
    def crew(self) -> Crew:
        """Create the sequential research crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


def create_crew() -> tuple[Crew, Task]:
    """Build the crew and return its summary task for CLI validation."""
    project = ResearchAssistant()
    return project.crew(), project.summary_task()


def source_urls(text: str) -> list[str]:
    """Return unique HTTP(S) URLs found in a report, preserving their order."""
    urls = (url.rstrip(".,;:") for url in SOURCE_URL_PATTERN.findall(text))
    return list(dict.fromkeys(urls))
