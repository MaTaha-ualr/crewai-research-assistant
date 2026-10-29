# CrewAI learning notes and ticket reference

This file keeps the original notes and code examples below. The examples are
formatted as separate Markdown code blocks; their wording and code are retained
as originally recorded, including incomplete or older snippets. New, complete
answers to the ticket review questions are in
[docs/questions-and-answers.md](docs/questions-and-answers.md), and concise
project-specific concept definitions are in [docs/crewai-concepts.md](docs/crewai-concepts.md).

The older examples that mention OpenAI models, Serper, or Flow APIs describe
those original documentation excerpts; they are not the configuration used by
this repository. This project uses local Ollama inference and Exa web search.

## Original notes

Trade off between the complexity - precision
for the decision to cchoose between the crew or a flow

https://docs.crewai.com/v1.15.32/en/guides/concepts/evaluating-use-cases



## Choosing between a Crew and a Flow

# complexity
> no. of distinct steps
> diversity of tasks that need to be performed
> interdependence of the different components
> conditional logic and branching
> sophistication of the overall workflow

# precision
> accuracy of the final output
> need for the strucctured and predictable results
> importance of reproducibility
> level of control over each step
> tolerrance of outputs


Low complexxity, Low precision
simple task - Creative or exploratory applications
>>>> Recommended Approach: Simple Crews with minimal agents

Low complexity, High precission
structured data extraction and transformation - simple classiication task
>>>> Recommended Approach: Flows with direct LLM calls or simple Crews with structured outputs

High complexity, Low precission
multi-stage process with many steps - creative or exploritory outputs - tolerance of various results
>>>> Recommended Approach: Complex Crews with multiple specialized agents

High ccomplexity, High Precission
complex workflows, with strucctured outputs - example: Enterprice decission support systems; multi stage document processing

### When a Crew fits

Crews 
>> Need collabaration between the specalized agent.
>> the task is creative or analytical
>> the output format can be somewhat flexxible

example of crews:
```python
# Example: Research Crew for market analysis
from crewai import Agent, Crew, Process, Task

# Create specialized agents
researcher = Agent(
    role="Market Research Specialist",
    goal="Find comprehensive market data on emerging technologies",
    backstory="You are an expert at discovering market trends and gathering data."
)

analyst = Agent(
    role="Market Analyst",
    goal="Analyze market data and identify key opportunities",
    backstory="You excel at interpreting market data and spotting valuable insights."
)

# Define their tasks
research_task = Task(
    description="Research the current market landscape for AI-powered healthcare solutions",
    expected_output="Comprehensive market data including key players, market size, and growth trends",
    agent=researcher
)

analysis_task = Task(
    description="Analyze the market data and identify the top 3 investment opportunities",
    expected_output="Analysis report with 3 recommended investment opportunities and rationale",
    agent=analyst,
    context=[research_task]
)

# Create the crew
market_analysis_crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    process=Process.sequential,
    verbose=True
)

# Run the crew
result = market_analysis_crew.kickoff()
```

### When a Flow fits

Flows:
>> need precise sequencing and state management.
>>structured and predictable oututs
>> the workflow involves conditional logic
>> the solution requires both ai capabilities and traditional

```python
# Example: Customer Support Flow with structured processing
from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel
from typing import List, Dict

# Define structured state
class SupportTicketState(BaseModel):
    ticket_id: str = ""
    customer_name: str = ""
    issue_description: str = ""
    category: str = ""
    priority: str = "medium"
    resolution: str = ""
    satisfaction_score: int = 0

class CustomerSupportFlow(Flow[SupportTicketState]):
    @start()
    def receive_ticket(self):
        # In a real app, this might come from an API
        self.state.ticket_id = "TKT-12345"
        self.state.customer_name = "Alex Johnson"
        self.state.issue_description = "Unable to access premium features after payment"
        return "Ticket received"

    @listen(receive_ticket)
    def categorize_ticket(self, _):
        # Use a direct LLM call for categorization
        from crewai import LLM
        llm = LLM(model="openai/gpt-4o-mini")

        prompt = f"""
        Categorize the following customer support issue into one of these categories:
        - Billing
        - Account Access
        - Technical Issue
        - Feature Request
        - Other

        Issue: {self.state.issue_description}

        Return only the category name.
        """

        self.state.category = llm.call(prompt).strip()
        return self.state.category

    @router(categorize_ticket)
    def route_by_category(self, category):
        # Route to different handlers based on category
        return category.lower().replace(" ", "_")

    @listen("billing")
    def handle_billing_issue(self):
        # Handle billing-specific logic
        self.state.priority = "high"
        # More billing-specific processing...
        return "Billing issue handled"

    @listen("account_access")
    def handle_access_issue(self):
        # Handle access-specific logic
        self.state.priority = "high"
        # More access-specific processing...
        return "Access issue handled"

    # Additional category handlers...

    @listen(or_("billing", "account_access", "technical_issue", "feature_request", "other"))
    def resolve_ticket(self, resolution_info):
        # Final resolution step
        self.state.resolution = f"Issue resolved: {resolution_info}"
        return self.state.resolution

# Run the flow
support_flow = CustomerSupportFlow()
result = support_flow.kickoff()
```

### Combining Crews and Flows

When to Combine Crews and Flows:
> use flows to orchestrate the overall process and crews for complex subtasks
> use cres for creative tasks and flows for structured processing
> flows to manage state and process flow while leveraging Crews for speaclied work.



## Designing agents and tasks

crafting effective Agents
https://docs.crewai.com/v1.15.32/en/guides/agents/crafting-effective-agents

agent - a specalized ai entity designed to perfform specific roles within a collbarative framework.

>>>> well designed agents produce more relevant, high quality results
>>>> agent with complementary skills work together more efficiently
>>>> agents with clear roles and goals execute tasks more effectively
>>>> thoughtfully designed agents can be reused acreoss multiple crews and contexts

80/20 rule:
80% of the effort sould go into desigining tasks, and 20% of the time into defining agents
Role:
agents must be specific and specalized: Instead of writer - Senior UX REasercher in user interview analysis
align with real world professions
specify the agents fiield of knowledge

Goal:
effective goals must be clear and outcoe focused
emphaasize quality standards - the expectations
incorporate success criteria - what good looks like define it 
example of a goal: goal: "Uncover actionable user insights by analyzing interview data and identifying recurring patterns, unmet needs, and improvement opportunities"

Backstory: 
explain how the agent gained their skills
define how the agents approaches their work
create a cohesive persoas
examle of a backstory:
backstory: "With 20+ years of experience building distributed systems at scale, you've developed a pragmatic approach to software architecture. You've seen both successful and failed systems and have learned valuable lessons from each. You balance theoretical best practices with practical constraints and always consider the maintenance and operational aspects of your designs."


Effective agents are a perffecct balance between specalizations - doing one thing extremely well and versatillity being adaptive to various situations

bad example
role: "Writer"
goal: "Write good content"
backstory: "You are a writer who creates content for websites."

good example
role: "B2B Technology Content Strategist"
goal: "Create compelling, technically accurate content that explains complex topics in accessible language while driving reader engagement and supporting business objectives"
backstory: "You have spent a decade creating content for leading technology companies, specializing in translating technical concepts for business audiences. You excel at research, interviewing subject matter experts, and structuring information for maximum clarity and impact. You believe that the best B2B content educates first and sells second, building trust through genuine expertise rather than marketing hype."


Task design best practices:

1. Single purpose, Single output
2. be explicit about inputs and outputs
3. explain the purpose ad the context
4. for machine readale outputs, specify the format clearly

common mistakes to avoid:
1. unclear task instrucctions
2. "GOD tasks" taht try to do too much
3. Misaligned description and expeted output
4. not understandin the process yourself - try to perform the task manulally first
- document the process, decision points, and information sourcces
- use the documentation as the basis for yout task description
5. premature use of hierarchial structures - start with the sequential process and only move to hierarcchial models when the workflow complexity truly reqires it.
6. Vague or generic agent definations


Testing and iterating on agent design
sstart with a prototype:
test with sample tasks
analyze outputs
refiinie the definations
test in collaboration

## Sequential process notes

# https://docs.crewai.com/v1.15.32/en/learn/sequential-process

CrewAI offers a flexible framework for executing tasks in a structured manner, supporting both sequential and hierarchical processes. 

Sequential Process - ensures tasks are executed one after the other, following a linear progression.

Define your agent

```python
researcher = agent(
    role = ''
    goal = ''
    backstory = ''
)

Deine our tasks 

research_tassk = Task(
    description = 
    agent = researcher,
    expected_output = 'Raw Data'
)

form the crew with a sequential process
report_crew = Crew(
    agents = [research]
    tasks = [research_task]
    process = Process.sequential
    > process = Process.hierarchial
        manager_llm = "gpt-4o"
        planning = True

        the manager could also be a custom agent
        role 
        goal
        backstory
        allow_delegation = True
        
)

# execute the crew
result = report_crew.kickoff()

# accessing the type-safe output
task_output: TaskOutput = result.task[0].output
crew_output: CrewOutput = result.output
```





## Ticket review questions (original notes)

Questions to Answer
Answer these questions in docs/questions-and-answers.md:

What is CrewAI?
> Open source framework for orchestrating autonomous ai agents and building complex workflows.
> It helps to build the multi-agent systems by combining the collaborative intelligence of crews witht the precise control of Flows.

What is the difference between an agent and a task?
> a task is a specific assignment completed by an Agent. 
What is a crew?
> Crews are teams of autonomous agents that collaborate to solve specific tasks delegated to them by the Flow.

Why are two agents used instead of one agent doing everything?

What does a sequential process do?
> executing of tasks can be done iiin a structured manner, supporting both sequential and hierarchial processes
sequential: tasks are executed one after the other, following a linear progression. 
Example of a sequential process
```python
from crewai import Crew, Process, Agent, Task, TaskOutput, CrewOutput

# Define your agents
researcher = Agent(
  role='Researcher',
  goal='Conduct foundational research',
  backstory='An experienced researcher with a passion for uncovering insights'
)
analyst = Agent(
  role='Data Analyst',
  goal='Analyze research findings',
  backstory='A meticulous analyst with a knack for uncovering patterns'
)
writer = Agent(
  role='Writer',
  goal='Draft the final report',
  backstory='A skilled writer with a talent for crafting compelling narratives'
)

# Define your tasks
research_task = Task(
  description='Gather relevant data...', 
  agent=researcher, 
  expected_output='Raw Data'
)
analysis_task = Task(
  description='Analyze the data...', 
  agent=analyst, 
  expected_output='Data Insights'
)
writing_task = Task(
  description='Compose the report...', 
  agent=writer, 
  expected_output='Final Report'
)

# Form the crew with a sequential process
report_crew = Crew(
  agents=[researcher, analyst, writer],
  tasks=[research_task, analysis_task, writing_task],
  process=Process.sequential
)

# Execute the crew
result = report_crew.kickoff()

# Accessing the type-safe output
task_output: TaskOutput = result.tasks[0].output
crew_output: CrewOutput = result.output
```


How does the Summary Agent receive the Research Agent's findings?

What is the purpose of a tool?

How would you add another agent to verify the sources?

What happens when the search tool fails?

How would you reduce unnecessary model calls and execution costs?


## Agent reference notes

https://docs.crewai.com/v1.15.33/en/concepts/agents
an Agent is an autonomous unit that can:
Attribute	Parameter	Type	Description
Role	role	str	Defines the agent’s function and expertise within the crew.
Goal	goal	str	The individual objective that guides the agent’s decision-making.
Backstory	backstory	str	Provides context and personality to the agent, enriching interactions.

```python
from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent with all available parameters
agent = Agent(
    role="Senior Data Scientist",
    goal="Analyze and interpret complex datasets to provide actionable insights",
    backstory="With over 10 years of experience in data science and machine learning, "
              "you excel at finding patterns in complex datasets.",
    llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4"
    function_calling_llm=None,  # Optional: Separate LLM for tool calling
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    max_iter=20,  # Default: 20 iterations
    max_rpm=None,  # Optional: Rate limit for API calls
    max_execution_time=None,  # Optional: Maximum execution time in seconds
    max_retry_limit=2,  # Default: 2 retries on error
    allow_code_execution=False,  # Default: False
    code_execution_mode="safe",  # Default: "safe" (options: "safe", "unsafe")
    respect_context_window=True,  # Default: True
    use_system_prompt=True,  # Default: True
    multimodal=False,  # Default: False
    inject_date=False,  # Default: False
    date_format="%Y-%m-%d",  # Default: ISO format
    reasoning=False,  # Default: False
    max_reasoning_attempts=None,  # Default: None
    tools=[SerperDevTool()],  # Optional: List of tools
    knowledge_sources=None,  # Optional: List of knowledge sources
    embedder=None,  # Optional: Custom embedder configuration
    system_template=None,  # Optional: Custom system prompt template
    prompt_template=None,  # Optional: Custom prompt template
    response_template=None,  # Optional: Custom response template
    step_callback=None,  # Optional: Callback function for monitoring
)
```

# critical parameters
role, goal, backstory

# memeory and context parameters
memeory, respect_context_window, knowledge_source

# execution control
max_iter, max_execution_time, max_rpm(rate limiting for api calls), max_Retry_limit


The kickoff() method allows you to send messages directly to an agent and get a response, similar to how you would interact with an LLM but with all the agent’s capabilities (tools, reasoning, etc.).

```python
from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[SerperDevTool()],
    verbose=True
)

# Use kickoff() to interact directly with the agent
result = researcher.kickoff("What are the latest developments in language models?")

# Access the raw response
print(result.raw)
```

## Agent capability notes

https://docs.crewai.com/v1.15.33/en/concepts/agent-capabilities
CrewAI agents can be extended with five distinct capability types
Tools - Callable functions - give aents the ability to take action. Web searches, file operations, api calls, code execution.

MCP servers - Remote tool servers - coneect agets to external tool servers via the Model Context Protocol. Same effect as tools, but hosted externally.

Apps Platfors integrations

Skills Domain expertise - inject instrutions, guidelines, and reference material into agent prompts. Skills tell agents how to think.

Knowledge Retrieved facts - provide agents with data from documentation via semantic search RAG

```python
from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool

from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool, CodeInterpreterTool

# A fully-equipped research agent
researcher = Agent(
    role="Senior Research Analyst",
    goal="Produce comprehensive market analysis reports",
    backstory="Expert analyst with deep industry knowledge",

    # ACTION: What the agent can DO
    tools=[
        SerperDevTool(),         # Search the web
        FileReadTool(),          # Read local files
        CodeInterpreterTool(),   # Run Python code for analysis
    ],
    mcps=["https://data-api.example.com/sse"],  # Access remote data API
    apps=["google_sheets"],                      # Write to Google Sheets

    # CONTEXT: What the agent KNOWS
    skills=["./skills/research-methodology"],    # How to conduct research
    knowledge_sources=[company_docs],            # Company-specific data
)
```

## Task reference notes

https://docs.crewai.com/v1.15.33/en/concepts/tasks

a Task is a specific assignment completed by an Agent.
all necessary details for execution, descrition, agent responsible, required tools.

Tasks can be executed in two ways:
Sequential: Tasks are executed in the order they are defined
Hierarchical: Tasks are assigned to agents based on their roles and expertise

Task Attributes
Attribute	Parameters	Type	Description
Description	description	str	A clear, concise statement of what the task entails.
Expected Output	expected_output	str	A detailed description of what the task’s completion looks like.


Task Guardrails - a way to validate and transform task outputs before they are passed to the next task
Function-based guardrails: Python functions with custom validation logic, giving you complete control over the validation process and ensuring reliable, deterministic results.
LLM-based guardrails: String descriptions that use the agent’s LLM to validate outputs based on natural language criteria. These are ideal for complex or subjective validation requirements.

Asynchronous Execution
You can define a task to be executed asynchronously. This means that the crew will not wait for it to be completed to continue with the next task. This is useful for tasks that take a long time to be completed, or that are not crucial for the next tasks to be performed.
You can then use the context attribute to define in a future task that it should wait for the output of the asynchronous task to be completed.

```python
list_ideas = Task(
 async_execution=True # Will be executed asynchronously
)
list_important_history = Task(
  async_execution=True # Will be executed asynchronously
)

write_Article = Task(
    context=[list_ideas, list_important_history] # Will wait for the output of the two tasks to be completed

)
```

## Crew reference notes

https://docs.crewai.com/v1.15.33/en/concepts/crews
A crew in crewAI represents a collaborative group of agents working together to achieve a set of tasks. Each crew defines the strategy for task execution, agent collaboration, and the overall workflow.
Example crew.jsonc
```jsonc
{
  "name": "Market Research Crew",
  "agents": ["researcher", "analyst"],
  "tasks": [
    {
      "name": "research",
      "description": "Research {topic} and collect the most relevant facts.",
      "expected_output": "Structured research notes about {topic}.",
      "agent": "researcher"
    },
    {
      "name": "analysis",
      "description": "Analyze the research and write a concise report.",
      "expected_output": "A markdown report with findings and recommendations.",
      "agent": "analyst",
      "context": ["research"],
      "output_file": "output/report.md"
    }
  ],
  "process": "sequential",
  "verbose": true,
  "memory": true,
  "inputs": {
    "topic": "AI Agents"
  }
}
```

## Flow reference notes

https://docs.crewai.com/v1.15.33/en/concepts/flows
