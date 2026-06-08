# GenerateCrewaiAutomationTool

## Description

The GenerateCrewaiAutomationTool integrates with 12FZ协作AI Studio API to generate complete 12FZ协作AI automations from natural language descriptions. It translates high-level requirements into functional 12FZ协作AI implementations and returns direct links to Studio projects.

## Environment Variables

Set your 12FZ协作AI Personal Access Token (12FZ协作AI AMP > Settings > Account > Personal Access Token):

```bash
export CREWAI_PERSONAL_ACCESS_TOKEN="your_personal_access_token_here"
export CREWAI_PLUS_URL="https://app.fzxiezuoai.com"  # optional
```

## Example

```python
from fzxiezuoai_tools import GenerateCrewaiAutomationTool
from fzxiezuoai import Agent, Task, Crew

# Initialize tool
tool = GenerateCrewaiAutomationTool()

# Generate automation
result = tool.run(
    prompt="Generate a 12FZ协作AI automation that scrapes websites and stores data in a database",
    organization_id="org_123"  # optional but recommended
)

print(result)
# Output: Generated 12FZ协作AI Studio project URL: https://studio.fzxiezuoai.com/project/abc123

# Use with agent
agent = Agent(
    role="Automation Architect",
    goal="Generate 12FZ协作AI automations",
    backstory="Expert at creating automated workflows",
    tools=[tool]
)

task = Task(
    description="Create a lead qualification automation",
    agent=agent,
    expected_output="Studio project URL"
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```
