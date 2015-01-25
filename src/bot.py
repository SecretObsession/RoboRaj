"""
Simple IRC Bot for Twitch.tv

Originally developed by Aidan Thomson <aidraj0@gmail.com>
Tweaks by Shane Engelman <me@5h4n3.com>
Forked and updated by Mike Herold <archangel.herold@gmail.com>
"""

import lib.irc as irc_
from lib.functions_general import *
import lib.functions_commands as commands
import sys
import datetime


class RoboRaj(object):
    def __init__(self, config):
        self.config = config
        self.irc = irc_.IRC(config)
        self.socket = self.irc.get_irc_socket_object()
        commands.load_commands_from_cache()
        commands.generate_last_used()

    def run(self):
        irc = self.irc
        sock = self.socket
        config = self.config

        while True:
            data = sock.recv(config['socket_buffer_size']).rstrip()

            if len(data) == 0:
                print_bot_status_message('Connection was lost, reconnecting.')
                sock = self.irc.get_irc_socket_object()

            if config['debug']:
                print data

            # check for ping, reply with pong
            irc.check_for_ping(data)

            if irc.check_for_message(data):
                message_dict = irc.get_message(data)

                channel = message_dict['channel']
                message = message_dict['message']
                username = message_dict['username']

                print_chat_message_in_html(channel, message, username)

                # check if message is a command with no arguments
                if commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0]):
                    command = message

                    if commands.check_returns_function(command.split(' ')[0]):
                        if commands.check_has_correct_args(command, command.split(' ')[0]):
                            args = command.split(' ')
                            del args[0]

                            command = command.split(' ')[0]

                            if commands.is_on_cooldown(command, channel):
                                print_bot_message('Command is on cooldown. (%s) (%s) (%ss remaining)' % (command, username, commands.get_cooldown_remaining(command, channel)), channel)
                            else:
                                print_bot_message('Command is valid and it is not on cooldown. (%s) (%s)' % (command, username), channel)

                                result = commands.pass_to_function(command, args)
                                commands.update_last_used(command, channel)

                                if result:
                                    resp = '(%s) > %s' % (username, result)
                                    print_bot_message(resp, channel)
                                    irc.send_message(channel, resp)

                    else:
                        if commands.is_on_cooldown(command, channel):
                            print_bot_message('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                            command, username, commands.get_cooldown_remaining(command, channel)),
                                 channel
                            )
                        elif commands.check_has_return(command):
                            print_bot_message('Command is valid and not on cooldown. (%s) (%s)' % (
                            command, username),
                                 channel
                            )
                            commands.update_last_used(command, channel)

                            resp = '(%s) > %s' % (username, commands.get_return(command))
                            commands.update_last_used(command, channel)

                            print_bot_message(resp, channel)
                            irc.send_message(channel, resp)


#Logged in UTF-8
class Logger(RoboRaj):
    def __init__(self, config, filename="log/bot.log"):
        # this should be saved in bot.log
        super(Logger, self).__init__(config)
        self.terminal = sys.stdout
        sys.stdout = self
        self.log = open(filename, "a+")

    def write(self, message):
        #In the event of an error, "try", to prevent bot crash. If there is an error, print it
        try:
            safe_message = unicode(message).encode('utf8', 'ignore')
            self.terminal.write(safe_message)
            self.log.write(safe_message)
        except Exception as err:
            #Uncomment line below the print error to console when it occurs
            self.log.write("Unhandled error:\n" + str(err))
            import traceback
            #traceback.print_exc(file=self.log)
            #Log the console output to file as it comes in
        finally:
            self.log.flush()

