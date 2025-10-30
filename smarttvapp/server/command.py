"""
command.py
Defines the abstract base class for commands and concrete implementations.
"""
from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    """Abstract base class for all commands."""

    @abstractmethod
    def execute(self, tv, args: List[str]) -> str:
        """
        Execute the command with the given arguments.
        Parameters:
            tv: The SmartTV instance to operate on.
            args (List[str]): List of arguments for the command.
        Returns:
            str: Result of the command execution.
        """
        pass


class GetCommand(Command):
    """Command to get the current state of the TV."""

    def execute(self, tv, args: List[str]) -> str:
        """Get the current TV state."""
        # TODO: Implement the more granular get commands.
        return "Current state: " + "\n" + tv.get_state("full")


class SetPowerCommand(Command):
    """Command to set the power state of the TV."""

    def execute(self, tv, args: List[str]) -> str:
        """Set the power state (on/off)."""
        if len(args) != 1:
            return "Error: Power command requires exactly one argument (on/off)."

        try:
            tv.set_power(args[0])
            return "state " + tv.get_state("full")
        except Exception as e:
            return f"Error: {e}"


class SetChannelCommand(Command):
    """Command to set the channel of the TV."""

    def execute(self, tv, args: List[str]) -> str:
        """Set the channel (up/down)."""
        if len(args) != 1:
            return "Error: Channel command requires exactly one argument (up/down)."

        try:
            tv.set_channel(args[0])
            return "state " + tv.get_state("full")
        except Exception as e:
            return f"Error: {e}"


class CommandFactory:
    """Factory class to create command instances."""

    @staticmethod # TODO: Learn how Python uses tags where Java uses keywords.
    def create_command(command_type: str, attribute: str = None) -> Command:
        """
        Create a command instance based on the command type and attribute.

        Parameters:
            command_type (str): The type of command ('get' or 'set').
            attribute (str): The attribute for set commands ('power' or 'channel').

        Returns:
            Command: The appropriate command instance.

        Raises:
            ValueError: If the command type or attribute is invalid.
        """
        if command_type == "get":
            return GetCommand()
        elif command_type == "set":
            if attribute == "power":
                return SetPowerCommand()
            elif attribute == "channel":
                return SetChannelCommand()
            else:
                raise ValueError(f"Unknown attribute: {attribute}. Use 'power' or 'channel'.")
        else:
            raise ValueError(f"Unknown command: {command_type}. Use 'get' or 'set'.")
