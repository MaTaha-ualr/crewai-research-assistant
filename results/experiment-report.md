# Five-topic experiment report

Run date: 2026-10-29T13:18:16-05:00
Total elapsed time: 438.7 seconds

| Topic | Research task | Source URLs | Findings section | Elapsed time | Errors |
| --- | --- | ---: | --- | ---: | --- |
| Latest developments in Model Context Protocol (MCP) | Completed | 2 | Present | 97.7s | None |
| CrewAI sequential process and task context | Completed | 4 | Present | 76.1s | None |
| Python environment variables documentation | Completed | 5 | Present | 76.6s | None |
| Recent Gemini API model updates | Completed | 1 | Present | 121.0s | None |
| Exa web search API documentation | Completed | 11 | Present | 67.3s | None |

## Research summaries

### Latest developments in Model Context Protocol (MCP)

# Summary of Latest Developments in Model Context Protocol (MCP)

## Key Findings

*   **Specification Update (November 25, 2025):** The MCP specification was updated to introduce significant operational and security enhancements across multiple SEPs.
*   **Task Tracking (SEP-1686):** An experimental feature was introduced to track multi-step operations with lifecycle states including `working`, `input_required`, `completed`, `failed`, and `cancelled`. This enables active polling by clients for task status and results.
```text
Lifecycle States: working, input_required, completed, failed, cancelled
```
*   **Authorization & Security:** Updates include OAuth extensions for machine-to-machine scenarios (SEP-1046) and Enterprise IdP policy controls (SEP-990). URL mode elicitation (SEP-1036) allows secure credential acquisition via browser OAuth flows without exposing credentials directly to clients.
*   **Schema & Tooling Standards:** The release adopts JSON Schema 2020-12 as the default dialect for MCP schemas. SEP-1330 standardized ElicitResult and EnumSchema support (titled, untitled, single/multi-select). Additionally, tool calling sampling is supported via `tools` and `toolChoice` parameters (SEP-1577) with a release candidate deadline of November 11th for validation testing.

## Conclusion
The MCP Specification's November 2025 version establishes critical improvements in multi-step task management, secure authentication flows, and schema standardization. These developments are designed to better support enterprise environments, client-side authorization, and complex operation tracking while maintaining security against credential exposure. Implementation is currently supported through release candidates available for a 14-day validation window prior to the November 25th full release.

## Source URLs

*   Model Context Protocol Blog \

### CrewAI sequential process and task context

# CrewAI Sequential Process and Task Context Research Summary

## Key Findings

### Task Configuration Requirements
*   Tasks in **CrewAI** support two execution modes: **Sequential** (defined order) or **Hierarchical** (assigned by roles). Execution is defined when creating a **Crew** with the `process` parameter set to `Process.sequential` or `Process.hierarchical`.
*   Every task requires specific parameters, including an **agent**, **description**, and `expected_output`.
*   Task context defines inputs from prior tasks. The `context` parameter specifies outputs from previous tasks that should be used in subsequent steps. Forward references are rejected to ensure sequential context remains explicit. Customization of context is managed via the `context` parameter in the `Task` class.

### Sequential Process Mechanics
*   Execution follows a **linear progression** where tasks run one after another.
*   The output of one task serves as the context for the next, ideal for projects requiring strict order.
*   To implement sequential processes:
    1.  Assemble agents and define tasks in execution order.
    2.  Create a **Crew** with `process=Process.sequential`.
    3.  Execute using the `kickoff()` method.

### Result Access and Execution API
*   Individual task outputs are accessed via: `result.tasks[index].output`.
*   Overall crew output is accessed via: `result.output`.

## Conclusion
Sequential processes in CrewAI enforce a strict, linear workflow where **task** A feeds directly into **task** B. This architecture ensures dependencies are managed explicitly through the **context** parameter while maintaining clear control over execution flow using the `process` and `kickoff()` methods.

## Sources
*   https://docs.crewai.com/v1.15.29/en/concepts/tasks  
    *(Source: CrewAI Documentation - Tasks, v1.15.29)*
*   https://docs.crewai.com/edge/en/learn/sequential-process  
    *(Source: CrewAI Documentation - Sequential Processes, Edge)*
*   https://docs.crewai.com/v1.15.29/en/learn/sequential-process  
    *(Source: CrewAI Documentation - Sequential Processes, v1.15.29)*
*   https://docs.crewai.com/v1.15.28/en/concepts/processes  
    *(Source: CrewAI Documentation - Processes, v1.15.28)*

### Python environment variables documentation

# Summary of Python Environment Variables Documentation

### Key Findings

*   **`NO_COLOR`**: Disables all color in Python interpreter output by defaulting to `TERM=dumb`. It takes precedence over `FORCE_COLOR` and `PYTHON_COLORS`, which follow the hierarchy `PYTHON_COLORS` > `NO_COLOR` > `FORCE_COLOR` [^1].
*   **`PYTHONHOME`**: Overrides standard library search paths (`prefix` and `exec_prefix`). A single directory replaces `/usr/local`. Separate values can be specified using `prefix:exec_prefix` format [^2].
*   **`PYTHONPATH`**: Extends the default search path for Python module imports. Uses colon (`:`) on Unix or semicolon (`;`) on Windows. Non-existent directories are ignored without error, and entries can reference zipfiles containing modules [^3].
*   **`PYTHONSTARTUP`**: Executes specified file commands before the interactive prompt in the current namespace (same scope). File contents trigger an auditing event `cpython.run_startup` [^4].
*   **`PYTHONOPTIMIZE`**: Configures interpreter optimization levels equivalent to `-O` flags. Setting it to a non-empty string enables one level (`-O`), while an integer value (e.g., `2`) enables multiple levels (`-O2`) [^5].

### Conclusion

The supplied research confirms the existence and specific behaviors of five critical environment variables (`NO_COLOR`, `PYTHONHOME`, `PYTHONPATH`, `PYTHONSTARTUP`, `PYTHONOPTIMIZE') within the Python interpreter. All findings are consistently attributed to official documentation across Python versions 3.14.5 and 3.15.0, ensuring reliable configuration management for output formatting, imports, startup scripts, and performance [^6-^10].

### Source URLs

```python
https://docs.python.org/3/using/cmdline.html#controlling-color
https://docs.python.org/3/using/cmdline.html#pythonhome
https://docs.python.org/3/using/cmdline.html#pythonpath
https://docs.python.org/3/using/cmdline.html#pythonstartup
https://docs.python.org/3/using/cmdline.html#pythonoptimize
```

[^1]: https://docs.python.org/3/using/cmdline.html#controlling-color
[^2]: https://docs.python.org/3/using/cmdline.html#pythonhome
[^3]: https://docs.python.org/3/using/cmdline.html#pythonpath
[^4]: https://docs.python.org/3/using/cmdline.html#pythonstartup
[^5]: https://docs.python.org/3/using/cmdline.html#pythonoptimize
[^6-^10]: See sources

### Recent Gemini API model updates

# Recent Gemini API Model Updates Summary

## Key Findings

Research from Google AI for Developers Documentation outlines recent model updates and releases between late 2024 and mid-2025:

- **December 19, 2024:** Released **Gemini 2.0 Flash Thinking Mode** in public preview. This is a test-time compute model allowing users to see the thought process during response generation for stronger reasoning capabilities.
- **March 12, 2025:** Launched an experimental **Gemini 2.0 Flash** model capable of image generation and editing. Also released **`gemma-3-27b-it`**, available on AI Studio and via the Gemini API during the Gemma 3 launch.
- **February 25, 2025:** Released **`gemini-2.0-flash-lite`** as Generally Available (GA). Optimized for speed, scale, and cost efficiency. *(Source notes: "February 24 in main text, February 25 in search results")*
- **March 25, 2025:** Released **`gemini-2.5-pro-exp-03-25`**, a public experimental Gemini model with Thinking Mode always on by default.
- **April 4, 2025:** Released **`gemini-2.5-pro-preview-03-25`** with billing enabled. Allowed users to continue using `gemini-2.5-pro-exp-03-25` on the free tier.

## Conclusion

Recent updates demonstrate a trajectory focused on **multimodality** (e.g., image generation), **efficiency** (Flash Lite), and **advanced reasoning** (Thinking Mode). The API expands its availability tiers to include **Preview**, **Experimental**, and **GA** stages, moving the Gemini 2.5 Pro model from experimental to billing-enabled status within a single month by spring 2025.

## Source URLs

All findings reference the same official changelog page on Google's AI for Developers documentation:

- https://ai.google.dev/gemini-api/docs/changelog

### Exa web search API documentation

# Key Findings: Exa Web Search API Documentation

Based strictly on the supplied research, here are the consolidated key findings regarding the Exa Search API:

## Authentication and Endpoints
- **API Endpoint:** The search service is served at `https://api.exa.ai`.
- **Auth Headers:** Requires authentication via Bearer token (`Authorization: Bearer $EXA_API_KEY`) or an `x-api-key` header.
- **SDK Keys:** Official API keys can be created at the dashboard at `https://dashboard.exa.ai/api-keys`.

## Development Tools and SDKs
- **Hosted MCP Server:** Accessible via agents through `https://mcp.exa.ai/mcp` without local SDK implementation.
- **Python SDK:** Available as `exa-py`, installed via `pip install exa-py`.
- **JavaScript SDK:** Available as `exa-js`, installed via `npm install exa-js`.
- **Key Configuration:** Both SDKs read the API key from an environment variable named `EXA_API_KEY`.

## Documentation and Specifications
- **Primary Reference:** Main search endpoint documentation is at `https://exa.ai/docs/reference/search`. This provides curl commands with parameters like `query` and `contents: { highlights: true }`.
- **OpenAPI Specs:** Request and response schemas are derived from OpenAPI specifications found here:
    - https://exa.ai/docs/exa-spec.yaml
    - https://exa.ai/docs/team-management-spec.yaml

## Conclusion
The research indicates a structured API setup using `https://api.exa.ai` with strict authentication requirements. Developers have flexibility between SDK options (Python/JS/MCP) but must configure via the `EXA_API_KEY` environment variable. Core schema definitions are centralized in OpenAPI YAML files alongside detailed search endpoint reference guides. All citations above reflect only sources provided within the initial research context.

## Source URLs from Research
The following URLs were cited as source material for this summary:
```language
https://api.exa.ai
https://exa.ai/docs/llms.txt
https://dashboard.exa.ai/api-keys
https://mcp.exa.ai/mcp
https://exa.ai/docs/exa-spec.yaml
https://exa.ai/docs/team-management-spec.yaml
https://exa.ai/docs/reference/search
```

## Review

A findings section was present in each completed summary. This confirms that summaries returned findings, but does not independently verify factual accuracy or whether every main finding was included. Manually review sources before relying on the reports.

## Run notes

All five research and summary tasks completed without runtime errors. Qwen 3.5 4B used the Exa search tool locally orchestrated by CrewAI. The unique final-summary URL counts ranged from 1 to 11. The Gemini API topic produced findings focused on updates through mid-2025 because the researcher queried for 2024 and 2025.

## Recency prompt retest

After passing the current date/year to both agents and including source dates in Exa results, I reran `Latest Gemini API model updates`. The researcher queried current 2026 information and returned official Google AI documentation with October 2026 updates. A direct Exa query for 2026 model updates also returned the official Google AI changelog with an October 27, 2026 entry. The original five-topic run predates this prompt fix; rerun it to replace those baseline results. Facts in the retest still need source-by-source review.
