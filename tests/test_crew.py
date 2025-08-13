"""Unit tests for the cyber_crew.crew module."""

from crewai import Crew, Task
from crewai.agents.agent_builder.base_agent import BaseAgent

from cyber_crew.crew import CyberCrew

crew = CyberCrew()
crew_instance = crew.crew()


class TestCyberCrew:
    """Unit tests for the CyberCrew class."""

    def test_init(self) -> None:
        """Test the initialization of the CyberCrew class."""
        assert isinstance(crew_instance, Crew)

    def test_crew(self) -> None:
        """Test the crew property of the CyberCrew class."""
        assert all(isinstance(agent, BaseAgent) for agent in crew_instance.agents)
        assert all(isinstance(task, Task) for task in crew_instance.tasks)
