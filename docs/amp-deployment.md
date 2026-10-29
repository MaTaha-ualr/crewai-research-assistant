# Deploying this Crew to CrewAI AMP

This repository now has the classic CrewAI Python project shape documented for
AMP: `pyproject.toml` declares `type = "crew"`, the `@CrewBase` class and
`run()` entry point live under `src/crewai_research_assistant/`, and `uv.lock`
pins dependencies for reproducible builds.

## Prepare the repository

1. Install Python 3.10–3.13 and `uv`.
2. From the repository root, run `uv lock` to generate or refresh `uv.lock`.
3. Copy `.env.example` to `.env`, set `OPENAI_API_KEY` and `EXA_API_KEY`, then
   run `uv sync` and verify a local run.
4. Commit and push the project, including `pyproject.toml` and `uv.lock`. Keep
   `.env` out of Git; `.gitignore` excludes it.

## Deploy through the AMP website

1. Push this repository to GitHub.
2. Sign in to CrewAI AMP and connect the GitHub repository.
3. Select this project as the deployment source.
4. Add `OPENAI_API_KEY`, `EXA_API_KEY`, and `MODEL` in the deployment's
   environment-variable settings. Use `gpt-6-luna` for `MODEL` unless you have
   selected another supported OpenAI model. Store the API key as a secret.
5. Deploy, then inspect the deployment logs and run a small topic through the
   deployment interface.

The CLI workflow is also supported by CrewAI: authenticate with `crewai login`
and create a deployment with `crewai deploy create`. This repository has not
been deployed to an AMP account.

## Project entry points

- `crewai run` uses `crewai_research_assistant.main:run` and the `RESEARCH_TOPIC`
  environment setting (with a sample topic when unset).
- `crewai_research_assistant.main:kickoff(inputs)` accepts the research `topic`.
- `run_with_trigger` parses a JSON trigger payload containing a `topic`.

See the official [AMP preparation guide](https://docs-platform.crewai.com/platform/en/guides/prepare-for-deployment)
and [deploy guide](https://docs-platform.crewai.com/platform/en/guides/deploy-to-amp).
