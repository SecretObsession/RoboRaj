"""
Developed by Mike Herold <archangel.herold@gmail.com>
GitHub: <https://github.com/secretobsession/twitch-bot>
"""

from src.config.config import *
from src.lib.command import Command


def roboraj(roboraj):
    Commands = roboraj['Commands']
    Messages = roboraj['Messages']
    Users = roboraj['Users']
    Points = roboraj['Points']

    args = roboraj['command_info']['args']
    channel = roboraj['command_info']['channel']
    user = roboraj['command_info']['user']

    if args[0] == "grantpoints":
        #add points to user's current count
        current_points = Points.get_points(username=args[1], channel=channel)
        new_point_value = current_points + int(args[2])
        Points.set_points(username=args[1], channel=channel, points=new_point_value)

    elif args[0] == "removecommand":
        Commands.remove_command(command=args[1])
        return "Command removed"

    elif args[0] == "addcommand":
        command = args[1]
        # set a hardcoded limit because of having to deal with large strings and potential for quotes
        command_cooldown = 10
        response_message = ""

        for argindex in range(2, len(args)):
            response_message += " %s" % (args[argindex])

        new_command = {
            'limit': command_cooldown,
            'return': response_message.lstrip()
        }

        # add the new command to the available commands list
        new_command_key = "!"+command
        Commands.commands[new_command_key] = new_command
        Commands.save_command_memory()

        return "Added command as an available command"

    elif args[0] == "dump_users":
        user_list = Users.list_users(channel=channel)
        response = ''

        for user_info in user_list:
            response += '%s ' % user_info['username']

        return response