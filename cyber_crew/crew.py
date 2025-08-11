"""Crew management for the Cyber Crew."""

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class CyberCrew:
    """Cyber Crew orchestrator for agents and tasks."""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def manager_agent(self) -> Agent:
        """Return the Manager Agent."""
        return Agent(
            config=self.agents_config["manager_agent"],
            verbose=True,
        )

    @agent
    def recon_specialist(self) -> Agent:
        """Return the Recon Specialist Agent."""
        return Agent(
            config=self.agents_config["recon_specialist"],
            verbose=True,
        )

    @agent
    def vulnerability_analyst(self) -> Agent:
        """Return the Vulnerability Analyst Agent."""
        return Agent(
            config=self.agents_config["vulnerability_analyst"],
            verbose=True,
        )

    @agent
    def exploit_engineer(self) -> Agent:
        """Return the Exploit Engineer Agent."""
        return Agent(
            config=self.agents_config["exploit_engineer"],
            verbose=True,
        )

    @agent
    def access_broker(self) -> Agent:
        """Return the Access Broker Agent."""
        return Agent(
            config=self.agents_config["access_broker"],
            verbose=True,
        )

    @agent
    def privilege_escalator(self) -> Agent:
        """Return the Privilege Escalator Agent."""
        return Agent(
            config=self.agents_config["privilege_escalator"],
            verbose=True,
        )

    @agent
    def file_mapper(self) -> Agent:
        """Return the File Mapper Agent."""
        return Agent(
            config=self.agents_config["file_mapper"],
            verbose=True,
        )

    @agent
    def flag_hunter(self) -> Agent:
        """Return the Flag Hunter Agent."""
        return Agent(
            config=self.agents_config["flag_hunter"],
            verbose=True,
        )

    @agent
    def report_writer(self) -> Agent:
        """Return the Report Writer Agent."""
        return Agent(
            config=self.agents_config["report_writer"],
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def recon_task(self) -> Task:
        """Create the Recon Task."""
        return Task(
            config=self.tasks_config["recon_task"],
        )

    @task
    def vulnerability_analysis(self) -> Task:
        """Create the Vulnerability Analysis Task."""
        return Task(
            config=self.tasks_config["vulnerability_analysis"],
        )

    @task
    def exploitation(self) -> Task:
        """Create the Exploitation Task."""
        return Task(
            config=self.tasks_config["exploitation"],
        )

    @task
    def access_establishment(self) -> Task:
        """Create the Access Establishment Task."""
        return Task(
            config=self.tasks_config["access_establishment"],
        )

    @task
    def privilege_escalation(self) -> Task:
        """Create the Privilege Escalation Task."""
        return Task(
            config=self.tasks_config["privilege_escalation"],
        )

    @task
    def file_system_mapping(self) -> Task:
        """Create the File System Mapping Task."""
        return Task(
            config=self.tasks_config["file_system_mapping"],
        )

    @task
    def flag_extraction(self) -> Task:
        """Create the Flag Extraction Task."""
        return Task(
            config=self.tasks_config["flag_extraction"],
        )

    @task
    def report_writing(self) -> Task:
        """Create the Report Writing Task."""
        return Task(
            config=self.tasks_config["report_writing"],
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Create the CyberCrew crew."""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
