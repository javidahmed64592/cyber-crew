"""Crew management for the Cyber Crew."""

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, after_kickoff, agent, crew, task

from cyber_crew.tools.filesystem.check_file_exists import CheckFileExists
from cyber_crew.tools.filesystem.list_files import ListFiles
from cyber_crew.tools.filesystem.read_file import ReadFile
from cyber_crew.tools.network.fetch_url import FetchUrl
from cyber_crew.tools.network.gobuster_scan import GobusterScan
from cyber_crew.tools.network.nikto_scan import NiktoScan
from cyber_crew.tools.network.nmap_scan import NmapScan
from cyber_crew.tools.run_command import RunCommand
from cyber_crew.tools.vulnerability.find_suids import FindSuids
from cyber_crew.tools.vulnerability.search_exploit import SearchExploit

# Tools
check_file_exists = CheckFileExists()
list_files = ListFiles()
read_file = ReadFile()
fetch_url = FetchUrl()
gobuster_scan = GobusterScan()
nikto_scan = NiktoScan()
nmap_scan = NmapScan()
run_command = RunCommand()
find_suids = FindSuids()
search_exploit = SearchExploit()


@CrewBase
class CyberCrew:
    """Cyber Crew orchestrator for agents and tasks."""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Agents
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
            tools=[nmap_scan, nikto_scan, gobuster_scan, run_command],
            verbose=True,
        )

    @agent
    def vulnerability_analyst(self) -> Agent:
        """Return the Vulnerability Analyst Agent."""
        return Agent(
            config=self.agents_config["vulnerability_analyst"],
            tools=[search_exploit, run_command],
            verbose=True,
        )

    @agent
    def exploit_engineer(self) -> Agent:
        """Return the Exploit Engineer Agent."""
        return Agent(
            config=self.agents_config["exploit_engineer"],
            tools=[fetch_url, search_exploit, run_command],
            verbose=True,
        )

    @agent
    def access_broker(self) -> Agent:
        """Return the Access Broker Agent."""
        return Agent(
            config=self.agents_config["access_broker"],
            tools=[fetch_url, read_file, run_command],
            verbose=True,
        )

    @agent
    def privilege_escalator(self) -> Agent:
        """Return the Privilege Escalator Agent."""
        return Agent(
            config=self.agents_config["privilege_escalator"],
            tools=[find_suids, search_exploit, run_command],
            verbose=True,
        )

    @agent
    def file_mapper(self) -> Agent:
        """Return the File Mapper Agent."""
        return Agent(
            config=self.agents_config["file_mapper"],
            tools=[check_file_exists, list_files, run_command],
            verbose=True,
        )

    @agent
    def flag_hunter(self) -> Agent:
        """Return the Flag Hunter Agent."""
        return Agent(
            config=self.agents_config["flag_hunter"],
            tools=[check_file_exists, read_file, run_command],
            verbose=True,
        )

    @agent
    def report_writer(self) -> Agent:
        """Return the Report Writer Agent."""
        return Agent(
            config=self.agents_config["report_writer"],
            verbose=True,
        )

    # Tasks
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

    def report_writing(self) -> Task:
        """Create the Report Writing Task."""
        return Task(
            config=self.tasks_config["report_writing"],
            output_file="report.md",
        )

    # Kickoff
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

    @after_kickoff
    def write_summary_report(self) -> None:
        """Write a summary report after the crew has completed its tasks."""
        self.report_writer().execute_task(self.report_writing())
