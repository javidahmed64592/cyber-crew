"""Command line tools to interact with a file system."""

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
