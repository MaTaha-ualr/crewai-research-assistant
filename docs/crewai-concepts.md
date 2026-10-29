# CrewAI concepts for this project

This repository uses two agents, two tasks, one sequential Crew, and one search
tool. Model inference uses the OpenAI model selected by `MODEL`.

| Concept | Meaning in CrewAI | This project |
| --- | --- | --- |
| Agent | A configured AI worker with a role, goal, backstory, model, and optional tools. | The Research Specialist searches and records source evidence; the Research Summarizer writes from that evidence. |
| Task | A defined assignment with instructions and an expected output, assigned to an agent. | `research_task` finds evidence; `summary_task` produces a short sourced report. |
| Crew | A team of agents and tasks with a chosen execution process. | `ResearchAssistant.crew()` assembles the two agents and two tasks. |
| Tool | A callable capability an agent can use while carrying out a task. | The Research Specialist calls the Exa Search API through the Exa skill's documented request shape. |
| Process | The rule that determines the order and coordination of tasks. | `Process.sequential` runs research before summarization. |
| Output | The result produced by a task or by the full crew. | The final Markdown summary contains findings, a conclusion, and source URLs. |

The summary task receives the research task as `context`, so it can use the
research output without repeating the search. The project checks that the final
report is non-empty and contains at least one URL.

The repo's original learning notes, including raw examples, are retained in
[`learning.md`](../learning.md). Newer, complete answers to the ticket's review
questions are in [`questions-and-answers.md`](questions-and-answers.md).

## Official references

- [CrewAI Agents](https://docs.crewai.com/en/concepts/agents)
- [CrewAI Tasks](https://docs.crewai.com/en/concepts/tasks)
- [CrewAI Crews](https://docs.crewai.com/en/concepts/crews)
- [CrewAI Processes](https://docs.crewai.com/en/concepts/processes)
- [CrewAI Tools](https://docs.crewai.com/en/concepts/tools)
- [CrewAI LLMs](https://docs.crewai.com/en/concepts/llms)
