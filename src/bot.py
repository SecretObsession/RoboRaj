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
from lib.users import Users
from lib.twitch import Twitch
from lib.points import Points
import sys
import time
import logging


class RoboRaj():
    def __init__(self, config, log_filename="log/bot.log"):
        self.config = config
        self.irc = irc_.IRC(config)
        self.socket = self.irc.get_irc_socket_object()
        self.Command = Command(self.config)
        self.commands_dict = self.Command.get_commands()
        self.Messages = Messages(save_type="sqlite")
        self.Users = Users()
        self.Twitch = Twitch()
        self.Points = Points(config=self.config, users=self.Users)
        logging.basicConfig(filename=log_filename,
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def run(self):
        irc_stream = self.irc
        sock = self.socket
        config = self.config

        while True:
            data = sock.recv(config['socket_buffer_size']).rstrip()

            if len(data) == 0:
                logging.error('Connection was lost, reconnecting.')
                sock = self.irc.get_irc_socket_object()

            for data_event in data.splitlines():
                event_data = irc_stream.process_data(data_event)

                """
                Actions for when data is received on on the open IRC socket.
                """
                if irc_stream.is_join_message(event_data):
                    self.Users.add_to_channel(username=event_data['info']['username'],
                                              channel=event_data['info']['channel'])
                elif irc_stream.is_part_message(event_data):
                    self.Users.remove_from_channel(username=event_data['info']['username'],
                                                   channel=event_data['info']['channel'])
                elif irc_stream.is_mode_message(event_data):
                    channel = event_data['info']['channel']
                    username = event_data['info']['username']
                    if event_data['info']['status'] == 'op':
                        self.Users.update_mod_status(channel=channel, username=username, status=True)
                    if event_data['info']['status'] == 'deop':
                        self.Users.update_mod_status(channel=channel, username=username, status=False)
                elif irc_stream.is_list_message(event_data):
                    for user_info in event_data['info']['users']:
                        self.Users.add_to_channel(username=user_info["username"], channel=event_data['info']['channel'])
                elif irc_stream.is_priv_message(event_data):
                    timestamp = time.time()
                    channel = event_data['info']['channel']
                    message = event_data['info']['message']
                    username = event_data['info']['username']

                    self.Users.update(username, channel)

                    if config['debug']:
                        logging.debug("channel: %s | username: %s | message: %s" % (channel, username, message))

                    self.Messages.store_message(channel, username, message, timestamp)

                    # check if message is a command with no arguments
                    if self.Command.is_valid_command(message) or self.Command.is_valid_command(message.split(' ')[0]):
                        command = message
                        only_command = command.split(' ')[0]
                        command_user_level = self.Command.get_command_user_level(only_command)

                        if config['debug']:
                            logging.debug("command_class: %s", command_user_level)

                        if self.Command.is_authorized(command_user_level, username):
                            if self.Command.check_returns_function(command.split(' ')[0]):
                                if self.Command.check_has_correct_args(command, command.split(' ')[0]):
                                    args = command.split(' ')
                                    del args[0]

                                    command = command.split(' ')[0]
                                    if self.Command.is_on_cooldown(command, channel):
                                        cooldown_remaining = self.Command.get_cooldown_remaining(command, channel)
                                        logging.info('Command (%s) is on cooldown for user (%s) (%ss remaining)'
                                                     % (command, username, cooldown_remaining))
                                    else:
                                        logging.info('Command (%s) received by user (%s)'
                                                     % (command, username))
                                        result = self.Command.pass_to_function(command, args, channel,
                                                                               user=username,
                                                                               users=self.Users,
                                                                               messages=self.Messages,
                                                                               commands=self.Command,
                                                                               twitch=self.Twitch,
                                                                               points=self.Points)
                                        self.Command.update_last_used(command, channel)

                                        if result:
                                            resp = '(%s) > %s' % (username, result)
                                            print_bot_message(resp, channel)
                                            irc_stream.send_message(channel, resp)
                            else:
                                if self.Command.is_on_cooldown(command, channel):
                                    logging.info('Command (%s) is on cooldown for user (%s) (%ss remaining)'
                                                 % (command, username, self.Command.get_cooldown_remaining(command, channel)))
                                elif self.Command.check_has_return(command):
                                    logging.info('Command (%s) received by user (%s) on channel (%s)'
                                                 % (command, username, channel))
                                    self.Command.update_last_used(command, channel)

                                    resp = '(%s) > %s' % (username, self.Command.get_return(command))
                                    self.Command.update_last_used(command, channel)

                                    print_bot_message(resp, channel)
                                    irc_stream.send_message(channel, resp)
                        else:
                            irc_stream.send_message(channel, "User not authorized")
                            logging.info("(%s) Not authorized to run command." % (username,))
