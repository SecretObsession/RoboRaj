"""
Simple IRC Bot for Twitch.tv

Originally developed by Aidan Thomson <aidraj0@gmail.com>
Tweaks by Shane Engelman <me@5h4n3.com>
Forked and updated by Mike Herold <archangel.herold@gmail.com>
"""

import lib.irc as irc_
from lib.functions_general import *
from lib.command import Command
from lib.messages import Messages
import sys
import time
import logging


class RoboRaj():
    def __init__(self, config, log_filename="log/bot.log"):
        self.config = config
        self.irc = irc_.IRC(config)
        self.socket = self.irc.get_irc_socket_object()
        self.command_class = Command(self.config)
        self.commands_dict = self.command_class.get_commands()
        self.messages_class = Messages(save_type="sqlite")
        logging.basicConfig(filename=log_filename,
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def run(self):
        irc = self.irc
        sock = self.socket
        config = self.config

        while True:
            data = sock.recv(config['socket_buffer_size']).rstrip()

            if len(data) == 0:
                logging.error('Connection was lost, reconnecting.')
                sock = self.irc.get_irc_socket_object()

            # check for ping, reply with pong
            irc.check_for_ping(data)

            if irc.check_for_message(data):
                message_dict = irc.get_message(data)

                timestamp = time.time()
                channel = message_dict['channel']
                message = message_dict['message']
                username = message_dict['username']

                if config['debug']:
                    logging.debug("channel: %s | username: %s | message: %s" % (channel, username, message))

                self.messages_class.store_message(channel, username, message, timestamp)

                # check if message is a command with no arguments
                if self.command_class.is_valid_command(message) or self.command_class.is_valid_command(message.split(' ')[0]):
                    command = message
                    only_command = command.split(' ')[0]
                    command_user_level = self.command_class.get_command_user_level(only_command)

                    if config['debug']:
                        logging.debug("command_class: %s", command_user_level)

                    if self.command_class.is_authorized(command_user_level, username):
                        if self.command_class.check_returns_function(command.split(' ')[0]):
                            if self.command_class.check_has_correct_args(command, command.split(' ')[0]):
                                args = command.split(' ')
                                del args[0]

                                command = command.split(' ')[0]
                                if self.command_class.is_on_cooldown(command, channel):
                                    cooldown_remaining = self.command_class.get_cooldown_remaining(command, channel)
                                    logging.info('Command (%s) is on cooldown for user (%s) (%ss remaining)'
                                                 % (command, username, cooldown_remaining))
                                else:
                                    logging.info('Command (%s) received by user (%s)'
                                                 % (command, username))
                                    result = self.command_class.pass_to_function(command, args)
                                    self.command_class.update_last_used(command, channel)

                                    if result:
                                        resp = '(%s) > %s' % (username, result)
                                        print_bot_message(resp, channel)
                                        irc.send_message(channel, resp)
                        else:
                            if self.command_class.is_on_cooldown(command, channel):
                                logging.info('Command (%s) is on cooldown for user (%s) (%ss remaining)'
                                             % (command, username, self.command_class.get_cooldown_remaining(command, channel)))
                            elif self.command_class.check_has_return(command):
                                logging.info('Command (%s) received by user (%s) on channel (%s)'
                                             % (command, username, channel))
                                self.command_class.update_last_used(command, channel)

                                resp = '(%s) > %s' % (username, self.command_class.get_return(command))
                                self.command_class.update_last_used(command, channel)

                                print_bot_message(resp, channel)
                                irc.send_message(channel, resp)
                    else:
                        irc.send_message(channel, "User not authorized")
                        logging.info("(%s) Not authorized to run command." % (username,))
