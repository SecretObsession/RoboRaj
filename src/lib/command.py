"""
Command class that will manage the commands available to the bot.
"""
import time
import json
import importlib


class Command():
    def __init__(self, config):
        self.commands = {}
        self.config = config
        self.load_commands_from_cache()

    def is_valid_command(self, command):
        if command in self.commands:
            return True

    def get_command_user_level(self, command):
        try:
            return self.commands[command]['user_level']
        except KeyError:
            return "user"

    def is_authorized(self, required_user_level, username):
        if required_user_level == "user":
            return True
        try:
            user_group_config = self.config['user_groups'][required_user_level]
            if username in user_group_config['username']:
                return True
            else:
                return False
        except KeyError:
            return False

    def get_commands(self):
        return self.commands

    def remove_command(self, command):
        del self.commands[command]
        #update json cache
        self.save_command_memory()
        self.load_commands_from_cache()
        return True

    def generate_last_used(self):
        for channel in self.config['channels']:
            for command in self.commands:
                self.commands[command][channel] = {}
                self.commands[command][channel]['last_used'] = 0

    def update_last_used(self, command, channel):
        self.commands[command][channel]['last_used'] = time.time()

    def get_command_limit(self, command):
        return self.commands[command]['limit']

    def save_command_memory(self):
        # Initialize and save commands in memory to JSON file.
        command_json_file = open("src/res/commands.json", "w")
        command_json_file.write(json.dumps(self.commands, sort_keys=True))
        command_json_file.close()
        return True

    def load_commands_from_cache(self):
        # Load the commands JSON file
        with open("src/res/commands.json", "r") as command_json_file:
            content = command_json_file.read()

            # Update the commands variable in memory
            self.commands = json.loads(content)
        return True

    def is_on_cooldown(self, command, channel):
        try:
            if time.time() - self.commands[command][channel]['last_used'] < self.commands[command]['limit']:
                return True
        except KeyError:
            self.generate_last_used()
            if time.time() - self.commands[command][channel]['last_used'] < self.commands[command]['limit']:
                return True

    def get_cooldown_remaining(self, command, channel):
        return round(self.commands[command]['limit'] - (time.time() - self.commands[command][channel]['last_used']))

    def check_has_return(self, command):
        if self.commands[command]['return'] and self.commands[command]['return'] != 'command':
            return True

    def get_return(self, command):
        return self.commands[command]['return']

    def check_has_args(self, command):
        if 'argc' in self.commands[command]:
            return True

    def check_has_correct_args(self, message, command):
        message = message.split(' ')
        # allow overloading arguments (This is needed for !addtextresponse for long messages)
        if len(message) >= int(self.commands[command]['argc']):
            return True

    def check_returns_function(self, command):
        if self.commands[command]['return'] == 'command':
            return True

    def pass_to_function(self, command, args, channel,
                         user=None, users=None, commands=None, messages=None, twitch=None, points=None):
        command = command.replace('!', '')
        module = importlib.import_module('src.lib.commands.%s' % command)
        reload(module)
        function = getattr(module, command)
        roboraj_obj = {
            'Commands': commands,
            'Messages': messages,
            'Users': users,
            'TwitchAPI': twitch,
            'Points': points,
            'command_info': {
                'command': command,
                'args': args,
                'channel': channel,
                'user': user
            }
        }
        return function(roboraj_obj)