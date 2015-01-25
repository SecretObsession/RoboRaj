"""
Developed by Aiden
GitHub: <https://github.com/aidraj>
"""

from src.lib.command import Command
from src.config.config import *

def commands():
    usage = '!commands'
    commands_dict = Command(config).get_commands()

    return ", ".join(sorted(commands_dict))
