"""Tool to read a file."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


class ReadFileInput(BaseModel):
    """Input schema for ReadFile."""

    path: str = Field(..., description="The file path to read.")


class ReadFile(BaseTool):
    """Tool to read a file."""

    name: str = "Read File"
    description: str = "Tool to read a file."
    args_schema: type[BaseModel] = ReadFileInput

    def _run(self, path: str) -> str:
        cmd = f"cat {path}"
        return run_command(cmd)
