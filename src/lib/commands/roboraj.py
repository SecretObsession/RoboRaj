"""
Developed by Mike Herold <archangel.herold@gmail.com>
GitHub: <https://github.com/secretobsession/twitch-bot>
"""

from src.config.config import *
from src.lib.command import Command


def roboraj(robo_info):
    Commands = robo_info['Commands']
    Messages = robo_info['Messages']
    Users = robo_info['Users']

    args = robo_info['command_info']['args']
    channel = robo_info['command_info']['channel']
    user = robo_info['command_info']['user']
    #commands = Command(config)

    if args[0] == "removecommand":
        Commands.remove_command(command=args[1])
        return "Command removed"

    elif args[0] == "dump_users":
        user_list = Users.list_users(channel=channel)
        response = ''

        for user_info in user_list:
            response += '%s ' % user_info['username']

        return response