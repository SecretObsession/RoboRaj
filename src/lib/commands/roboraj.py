"""
Written by: Mike Herold <archangel.herold@gmail.com> <github.com/SecretObsession/>

RoboRaj command handler.
If a admin wants RoboRaj to run a task
-Update emotes from Twitch API
-Remove/Activate commands
"""

from src.config.config import *
from src.lib.command import Command

def roboraj(args):
    command = args[0]
    subcommand = args[1]
    commands = Command(config)

    if command == "removecommand":
        commands.remove_command(command=subcommand)
        return "Command removed"

    return True