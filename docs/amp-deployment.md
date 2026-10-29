# Deploying this Crew to CrewAI AMP

This repository now has the classic CrewAI Python project shape documented for
AMP: `pyproject.toml` declares `type = "crew"`, the `@CrewBase` class and
`run()` entry point live under `src/crewai_research_assistant/`, and `uv.lock`
pins dependencies for reproducible builds.

## Prepare the repository

1. Install Python 3.10–3.13 and `uv`.
2. From the repository root, run `uv lock` to generate or refresh `uv.lock`.
3. Run `uv sync` and verify a local run using a reachable Ollama server and
   `EXA_API_KEY` in `.env`.
4. Commit and push the project, including `pyproject.toml` and `uv.lock`. Keep
   `.env` out of Git; `.gitignore` excludes it.

## Deploy through the AMP website

1. Push this repository to GitHub.
2. Sign in to CrewAI AMP and connect the GitHub repository.
3. Select this project as the deployment source.
4. Add `EXA_API_KEY`, `MODEL`, and `OLLAMA_BASE_URL` in the deployment's
   environment-variable settings. Do not set `OLLAMA_BASE_URL` to localhost
   unless Ollama runs in the same deployed environment.
5. Deploy, then inspect the deployment logs and run a small topic through the
   deployment interface.

The CLI workflow is also supported by CrewAI: authenticate with `crewai login`
and create a deployment with `crewai deploy create`. This repository has not
been deployed to an AMP account.

## Ollama networking requirement

The local default `http://localhost:11434` works only when the Crew is running
on the same computer as Ollama. A hosted AMP worker's `localhost` points to that
worker, not to your development PC. For hosted execution, provide an Ollama
endpoint that AMP can reach and configure `OLLAMA_BASE_URL` accordingly, or use
another model endpoint reachable from AMP. Keep endpoint credentials in AMP's
environment settings. Qwen 3.5 4B remains the default model name; DeepSeek R1
1.5B can be selected with `MODEL=ollama/deepseek-r1:1.5b` when the hosted Ollama
server has that model available.

## Project entry points

- `crewai run` uses `crewai_research_assistant.main:run` and the `RESEARCH_TOPIC`
  environment setting (with a sample topic when unset).
- `crewai_research_assistant.main:kickoff(inputs)` accepts a `topic` and adds
  the current date and year before calling the Crew.
- `run_with_trigger` parses a JSON trigger payload containing a `topic`.

See the official [AMP preparation guide](https://docs-platform.crewai.com/platform/en/guides/prepare-for-deployment)
and [deploy guide](https://docs-platform.crewai.com/platform/en/guides/deploy-to-amp).
