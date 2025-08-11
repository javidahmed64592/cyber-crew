"""Tool to run a shell command."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


class RunCommandInput(BaseModel):
    """Input schema for RunCommand."""

    cmd: str = Field(..., description="The shell command to be executed.")


class RunCommand(BaseTool):
    """Tool to run a shell command."""

    name: str = "Run Command"
    description: str = "Tool to run a shell command."
    args_schema: type[BaseModel] = RunCommandInput

    def _run(self, cmd: str) -> str:
        return run_command(cmd)
