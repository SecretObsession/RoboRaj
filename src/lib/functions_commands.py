import time
import json

from src.config.config import *
from commands import *
from command_headers import *

import importlib


def is_valid_command(command):
    if command in commands:
        return True


def generate_last_used():
    for channel in config['channels']:
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0


def update_last_used(command, channel):
    commands[command][channel]['last_used'] = time.time()


def get_command_limit(command):
    return commands[command]['limit']


def save_command_memory(commands):
    # Initialize and save commands in memory to JSON file.
    command_json_file = open("src/res/commands.json", "w")
    command_json_file.write(json.dumps(commands, sort_keys=True, indent=4, separators=(',', ': ')))
    command_json_file.close()
    return True


def load_commands_from_cache():
    # Load the commands JSON file
    command_json_file = open("src/res/commands.json", "r")
    command_json_file.read()

    # Update the commands variable in memory
    commands = json.loads(command_json_file)
    command_json_file.close()
    return True


def is_on_cooldown(command, channel):
    if time.time() - commands[command][channel]['last_used'] < commands[command]['limit']:
        return True


def get_cooldown_remaining(command, channel):
    return round(commands[command]['limit'] - (time.time() - commands[command][channel]['last_used']))


def check_has_return(command):
    if commands[command]['return'] and commands[command]['return'] != 'command':
        return True


def get_return(command):
    return commands[command]['return']


def check_has_args(command):
    if 'argc' in commands[command]:
        return True


def check_has_correct_args(message, command):
    message = message.split(' ')
    # allow overloading arguments (This is needed for !addtextresponse for long messages)
    if len(message) >= int(commands[command]['argc']):
        return True


def check_returns_function(command):
    if commands[command]['return'] == 'command':
        return True


def pass_to_function(command, args):
    try:
        command = command.replace('!', '')
        module = importlib.import_module('src.lib.commands.%s' % command)
        reload(module)
        function = getattr(module, command)
        if args:
            if command == "addtextresponse":
                return function(args, commands)
            # need to reference to src.lib.commands.<command
            return function(args)
        else:
            # need to reference to src.lib.commands.<command
            return function()
    except:
        return 'Command Unavailable'