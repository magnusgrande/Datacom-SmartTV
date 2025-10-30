from command import CommandFactory


def parse_command(message):
    """Parse a client message and return a tuple: (command, attribute, value)
                                               or (command, None, None)
    """
    parts = message.strip().split()
    if not parts:
        return None, None, None
    command = parts[0]
    if command == "get":
        return "get", None, None
    elif command == "set" and len(parts) == 3:
        return "set", parts[1], parts[2]
    else:
        return None, None, None


def handle_protocol(tv, message):
    """Handle a client message using SmartTV and return a response string."""
    command_type, attribute, value = parse_command(message)

    if command_type is None:
        return "Error: Unknown command. Please try again."

    try:
        # Create the appropriate command using the factory
        command = CommandFactory.create_command(command_type, attribute)

        # Prepare arguments for the command
        args = []
        if value is not None:
            args = [value]

        # Execute the command
        return command.execute(tv, args)

    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
