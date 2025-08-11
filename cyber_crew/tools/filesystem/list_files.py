"""Tool to list the files in a directory."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


class ListFilesInput(BaseModel):
    """Input schema for ListFiles."""

    path: str = Field(..., description="The directory path to list files from.")


class ListFiles(BaseTool):
    """Tool to list the files in a directory."""

    name: str = "List Files"
    description: str = "Tool to list the files in a directory."
    args_schema: type[BaseModel] = ListFilesInput

    def _run(self, path: str) -> str:
        cmd = f"ls -Rla {path}"
        return run_command(cmd)
