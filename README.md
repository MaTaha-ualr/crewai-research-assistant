# CrewAI Research Assistant

A two-agent CrewAI research assistant. The Research Specialist uses Exa's web
search API to gather dated findings and source URLs. The Research Summarizer
receives that research as task context and produces a short report. Both agents
use the OpenAI model selected by `MODEL` (default: `gpt-6-luna`).

The repo uses CrewAI's classic Python/YAML project layout, with the project
metadata and entry point required by CrewAI AMP. Its research and summary
responsibilities remain in separate agent, task, tool, and crew modules.

## Requirements

- Python 3.10 through 3.13 (the CrewAI scaffold currently declares `<3.14`)
- An OpenAI API key for model inference
- An Exa API key for web search
- [uv](https://docs.astral.sh/uv/) for project and lockfile management

## Local setup

Create `.env` from `.env.example`, then set `OPENAI_API_KEY` and `EXA_API_KEY`.
The default model is selected by `MODEL`:

```powershell
uv sync
```

Run a topic:

```powershell
uv run python -m crewai_research_assistant.main "Latest developments in Model Context Protocol (MCP)"
```

Or use the CrewAI project entry point with the sample topic configured by
`RESEARCH_TOPIC` (defaults to recent MCP developments):

```powershell
uv run crewai run
```

Each run prints the report, source count, and elapsed time. It reports clear
errors for an empty topic, a failed search/model request, an empty report, or a
summary without source URLs. Exa search and OpenAI model inference make external
API requests.

## Run the five-topic experiment

```powershell
uv run python -m crewai_research_assistant.experiments
```

The runner prints progress and elapsed time for each topic, then writes the
observed results to `results/experiment-report.md`. It does not launch any
background or multi-hour job.

## Project structure

```text
pyproject.toml                         # AMP project type, dependencies, entry points
uv.lock                                # Reproducible dependency lock for AMP
src/crewai_research_assistant/
  agents.py                            # OpenAI LLM and agent construction
  tasks.py                             # Research and summary task construction
  tools.py                             # Exa search tool
  crew.py                              # AMP-compatible @CrewBase and sequential Crew
  main.py                              # AMP, CLI, and trigger entry points
  experiments.py                       # Five-topic experiment runner
  config/agents.yaml                   # Agent role, goal, and backstory
  config/tasks.yaml                    # Task instructions and expected outputs
docs/
  architecture.md
  amp-deployment.md
  crewai-concepts.md
  questions-and-answers.md
learning.md                            # Original notes and examples, organized
results/experiment-report.md           # Recorded experiment report
```

The summary task uses the research task as context, so the second agent does
not conduct the same search again. See the [architecture](docs/architecture.md),
[CrewAI concepts](docs/crewai-concepts.md), and [ticket answers](docs/questions-and-answers.md).

## CrewAI AMP

The source layout follows CrewAI's classic Python project structure. See
[docs/amp-deployment.md](docs/amp-deployment.md) for AMP setup and environment
variables.

## References

- [CrewAI AMP: Prepare for deployment](https://docs-platform.crewai.com/platform/en/guides/prepare-for-deployment)
- [CrewAI AMP: Deploy to AMP](https://docs-platform.crewai.com/platform/en/guides/deploy-to-amp)
- [CrewAI agents](https://docs.crewai.com/en/concepts/agents)
- [CrewAI tasks and context](https://docs.crewai.com/en/concepts/tasks)
- [CrewAI crews](https://docs.crewai.com/en/concepts/crews)
- [CrewAI processes](https://docs.crewai.com/en/concepts/processes)
- [CrewAI tools](https://docs.crewai.com/en/concepts/tools)
- [CrewAI LLMs](https://docs.crewai.com/en/concepts/llms)
- [OpenAI models](https://developers.openai.com/api/docs/models)
- [GPT-6 Luna model](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [Exa Search API](https://exa.ai/docs/reference/search)
- [Exa Python SDK](https://exa.ai/docs/sdks/python-sdk-specification)
- [Exa build-with-exa skill](https://github.com/exa-labs/agent-skills/tree/main/skills/build-with-exa)
- [uv project and lockfile guide](https://docs.astral.sh/uv/concepts/projects/)
