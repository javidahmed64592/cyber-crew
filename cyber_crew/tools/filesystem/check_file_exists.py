"""Tool to check a file's existence."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


class CheckFileExistsInput(BaseModel):
    """Input schema for CheckFileExists."""

    path: str = Field(..., description="The file path to check.")


class CheckFileExists(BaseTool):
    """Tool to check a file's existence."""

    name: str = "Check File Exists"
    description: str = "Tool to check a file's existence."
    args_schema: type[BaseModel] = CheckFileExistsInput

    def _run(self, path: str) -> str:
        cmd = f"test -f {path} && echo FOUND || echo NOT_FOUND"
        return run_command(cmd)
