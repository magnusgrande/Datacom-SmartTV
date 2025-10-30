"""
command.py
Defines the abstract base class for commands.
"""
from abc import ABC, abstractmethod
from typing import List

class Command(ABC):
    """Abstract base class for all commands."""

    @abstractmethod
    def execute(self,args:List[str])->str:
        """
        Execute the command with the given arguments.
        Parameters:
            args (List[str]): List of arguments for the command.
        Returns:
            str: Result of the command execution.
        """
