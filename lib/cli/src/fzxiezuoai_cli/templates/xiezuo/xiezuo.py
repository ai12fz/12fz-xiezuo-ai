from fzxiezuoai import Agent, Xiezuo, Process, Task
from fzxiezuoai.project import CrewBase, agent, xiezuo, task
from fzxiezuoai.agents.agent_builder.base_agent import BaseAgent


@XiezuoBase
class {{xiezuo_name}}():
    """{{xiezuo_name}} xiezuo"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @xiezuo
    def xiezuo(self) -> Xiezuo:
        """Creates the {{xiezuo_name}} xiezuo"""
        return Xiezuo(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
