# CrewAI review questions

These answers describe the implementation in this repository. The longer
learning notes and source examples are preserved in [`learning.md`](../learning.md).

## What is CrewAI?

CrewAI is an open-source Python framework for coordinating AI agents and
workflow steps. A Crew groups agents and tasks under an execution process. This
project uses a sequential Crew so a research task runs before a summary task.

## What is the difference between an agent and a task?

An **agent** is a configured worker with a role, goal, backstory, model, and
optional tools. A **task** is the specific assignment that worker must complete,
including its instructions and expected output. Here, the Research Specialist
is the agent; finding three to five dated findings with URLs is its task.

## What is a crew?

A Crew is the group of agents and tasks plus the process that coordinates them.
This Crew contains a Research Specialist and a Research Summarizer, with one
research task followed by one summary task.

## Why are two agents used instead of one agent doing everything?

The two roles separate evidence gathering from writing. This makes the handoff
clear: the Research Specialist searches and records sources, while the Research
Summarizer focuses on relevance, repetition, caveats, and readable structure.
The second agent receives the first task's output, which also prevents it from
duplicating the web search. One agent could do both jobs, but that would make
the responsibilities and quality checks less distinct.

## What does a sequential process do?

`Process.sequential` executes Crew tasks in their declared order. The research
task runs first; the summary task then uses its output as context. This is a
simple linear workflow, without a manager agent or branching.

## How does the Summary Agent receive the Research Agent's findings?

`summary_task` sets `context=[research_task]`. CrewAI passes the research task's
output into the summarizer's task context when the sequential Crew reaches that
step. The task instructions explicitly say to use that research and not search
again.

## What is the purpose of a tool?

A tool lets an agent take an action outside the model's text generation, such
as searching the web or reading a file. The Research Specialist's Exa tool
sends the query to Exa's Search API and returns titles, URLs, publication dates
when available, and highlights. The model uses those results as evidence; Exa
provides the live web search.

## How would you add another agent to verify the sources?

Add a verifier agent configuration and a verification task after research.
Give the verifier the research task as context and require it to check each
source URL, whether it supports the paired claim, and the publication date.
Then pass both research and verification outputs to the summary task. This adds
another model call, so it should be added only when independent verification is
needed and its cost is acceptable.

## What happens when the search tool fails?

An Exa request error is caught at the crew boundary and shown as a clear research
failure with a reminder to check the Exa credentials and model API settings. If
Exa returns no results, the tool returns an explicit no-results message, and
the task asks the Research Specialist to report that useful evidence was
unavailable. The CLI also reports an error if the final report is empty or has
no source URL.

## How would you reduce unnecessary model calls and execution costs?

- Keep only the two agents required by the workflow.
- Have the Research Specialist make the search call and tell the Summarizer to
  use its context instead of searching again.
- Ask for a bounded three-to-five findings and a concise report.
- Avoid memory, planning, hierarchical managers, and extra verification calls
  unless a demonstrated requirement justifies them.
- Use the selected OpenAI model for inference; Exa search is a separate hosted
  API call and may have its own usage cost.

## Does the model answer from memory or from the internet?

Both can influence the generated text, but current web evidence is supplied by
the Exa search tool. The Research Specialist is instructed to search for recent
topics and include URLs and dates; the Summarizer is instructed to use only that
research. The model's training knowledge is not a live news source, and Exa may
still return older pages or omit relevant pages. The report should therefore be
read with its source dates, and it should say when newer information was not
found. The project does not treat the model's own recollection as proof of a
current fact.

## Which API keys and model setting does this project need?

The active agents use OpenAI. Set `OPENAI_API_KEY` for model inference and
`MODEL` to the desired supported OpenAI model (the example defaults to
`gpt-6-luna`). Exa web search separately requires `EXA_API_KEY`. For AMP, add
these variables in the deployment's environment settings and store the keys as
secrets. Do not upload `.env` or expose keys in Git.

See the official [CrewAI AMP preparation guide](https://docs-platform.crewai.com/platform/en/guides/prepare-for-deployment)
and [deployment guide](https://docs-platform.crewai.com/platform/en/guides/deploy-to-amp).
