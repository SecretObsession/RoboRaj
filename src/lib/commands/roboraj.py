"""
Developed by Mike Herold <archangel.herold@gmail.com>
GitHub: <https://github.com/secretobsession/twitch-bot>
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