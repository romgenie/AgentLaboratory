from abc import ABC, abstractmethod


class Command(ABC):
    """Base abstract class for all command types."""
    
    def __init__(self):
        self.cmd_type = "OTHER"

    @abstractmethod
    def docstring(self) -> str:
        """Return the documentation string for the command."""
        pass

    @abstractmethod
    def execute_command(self, *args) -> str:
        """Execute the command with the given arguments."""
        pass

    @abstractmethod
    def matches_command(self, cmd_str) -> bool:
        """Check if the command string matches this command type."""
        pass

    @abstractmethod
    def parse_command(self, cmd_str) -> tuple:
        """Parse the command string into arguments for execution."""
        pass
