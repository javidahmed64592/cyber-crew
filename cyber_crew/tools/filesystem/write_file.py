"""Tool to write to a file."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class WriteFileInput(BaseModel):
    """Input schema for WriteFile."""

    path: str = Field(..., description="The file path to write to.")
    content: str = Field(..., description="The content to write to the file.")


class WriteFile(BaseTool):
    """Tool to write to a file."""

    name: str = "Write File"
    description: str = "Tool to write to a file."
    args_schema: type[BaseModel] = WriteFileInput

    def _run(self, path: str, content: str) -> str:
        with open(path, "w") as f:
            f.write(content)
        return f"Written to {path}"
