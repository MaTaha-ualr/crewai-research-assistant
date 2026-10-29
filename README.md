# CrewAI Research Assistant

A two-agent CrewAI research assistant. The Research Specialist uses Exa's web
search API to gather dated findings and source URLs. The Research Summarizer
receives that research as task context and produces a short report. Both agents
use a local Ollama model by default: `qwen3.5:4b`.

The repo uses CrewAI's classic Python/YAML project layout, with the project
metadata and entry point required by CrewAI AMP. Its research and summary
responsibilities remain in separate agent, task, tool, and crew modules.

## Requirements

- Python 3.10 through 3.13 (the CrewAI scaffold currently declares `<3.14`)
- [Ollama](https://ollama.com/download) installed and running
- The default `qwen3.5:4b` model pulled into Ollama
- An Exa API key for web search
- [uv](https://docs.astral.sh/uv/) for project and lockfile management

## Local setup

Create `.env` from `.env.example`, then set `EXA_API_KEY`. The model settings
default to Qwen 3.5 4B at Ollama's local endpoint:

```powershell
uv sync
ollama pull qwen3.5:4b
```

Keep Ollama running. You can optionally select DeepSeek R1 1.5B by pulling it
and setting `MODEL=ollama/deepseek-r1:1.5b` in `.env`. `OLLAMA_BASE_URL` defaults
to `http://localhost:11434`.

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
summary without source URLs. Exa search makes an external request; LLM inference
uses the configured Ollama endpoint.

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
  agents.py                            # Ollama LLM and agent construction
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

The source layout follows CrewAI's classic Python project structure. The
deployment process and the hosted Ollama requirement are in
[docs/amp-deployment.md](docs/amp-deployment.md). AMP must be able to reach the
configured Ollama endpoint; your local `localhost` is only for local runs.

## References

- [CrewAI AMP: Prepare for deployment](https://docs-platform.crewai.com/platform/en/guides/prepare-for-deployment)
- [CrewAI AMP: Deploy to AMP](https://docs-platform.crewai.com/platform/en/guides/deploy-to-amp)
- [CrewAI agents](https://docs.crewai.com/en/concepts/agents)
- [CrewAI tasks and context](https://docs.crewai.com/en/concepts/tasks)
- [CrewAI crews](https://docs.crewai.com/en/concepts/crews)
- [CrewAI processes](https://docs.crewai.com/en/concepts/processes)
- [CrewAI tools](https://docs.crewai.com/en/concepts/tools)
- [CrewAI LLMs](https://docs.crewai.com/en/concepts/llms)
- [CrewAI Ollama integration](https://docs.crewai.com/en/learn/llm-connections#ollama)
- [Ollama Qwen 3.5 model](https://ollama.com/library/qwen3.5)
- [Ollama DeepSeek R1 model](https://ollama.com/library/deepseek-r1)
- [Exa Search API](https://exa.ai/docs/reference/search)
- [Exa Python SDK](https://exa.ai/docs/sdks/python-sdk-specification)
- [Exa build-with-exa skill](https://github.com/exa-labs/agent-skills/tree/main/skills/build-with-exa)
- [uv project and lockfile guide](https://docs.astral.sh/uv/concepts/projects/)
