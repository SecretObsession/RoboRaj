import socket, re, time, sys
from functions_general import *
import cron
import thread


ping_no_response_threshold = 5 * 60  # five minutes, make this whatever you want


class IRC:
    def __init__(self, config):
        self.config = config
        self.sock = None

    def process_data(self, data):
        data_split = data.split(" ")

        # When the IRC client connects to a channel.
        if "PRIVMSG" in data_split[1]:
            event_information = {
                'event': 'message',
                'info': self.parse_message(data)
            }
            return event_information
        elif "PING" in data_split[0]:
            event_information = {
                'event': 'ping'
            }
            return event_information
        elif "PART" in data_split[1]:
            event_information = {
                'event': 'part',
                'info': self.parse_part(data)
            }
            return event_information
        elif "JOIN" in data_split[1]:
            event_information = {
                'event': 'join',
                'info': self.parse_join(data)
            }
            return event_information
        elif "MODE" in data_split[1]:
            event_information = {
                'event': 'mode',
                'info': self.parse_mode(data)
            }
            return event_information
        elif "353" in data_split[1]:
            event_information = {
                'event': 'list',
                'info': self.parse_channel_user_list(data)
            }
            return event_information
        else:
            return {'event': 'unknown'}

    def parse_channel_user_list(self, data):
        data_split = data.split("=")[1].lstrip().split(" ")
        channel = data_split[0]

        event_info = {'channel': channel, 'users': []}

        for user in data_split[1:]:
            user = user.lstrip(":")
            event_info['users'].append({'username': user})
        return event_info

    def parse_mode(self, data):
        status = ''
        if '+o' in data.split(" ")[3]:
            status = "op"
        elif '-o' in data.split(" ")[3]:
            status = "deop"

        channel = data.split(" ")[2]
        username = data.split(" ")[4]
        return {
            'status': status,
            'channel': channel,
            'username': username
        }

    def parse_part(self, data):
        nickname = data.split("!")[0].lstrip(":").rstrip('\r')
        username = data.split("!")[1].split("@")[0].rstrip('\r')
        channel = re.findall(r'PART #(.+)', data)[0]
        return {
            'nickname': nickname,
            'username': username,
            'channel': channel
        }

    def parse_join(self, data):
        nickname = data.split("!")[0].lstrip(":").rstrip('\r')
        username = data.split("!")[1].split("@")[0].rstrip('\r')
        channel = re.findall(r'JOIN (.+)', data)[0]
        return {
            'nickname': nickname,
            'username': username,
            'channel': channel
        }

    def parse_ping(self, data):
        last_ping = time.time()
        #if data[0:4] == "PING":
        if data.find('PING') != -1:
            self.sock.send('PONG ' + data.split()[1] + '\r\n')
            last_ping = time.time()
        if (time.time() - last_ping) > ping_no_response_threshold:
            sys.exit()

    def parse_message(self, data):
        return {
            'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
            'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
            'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0].decode('utf8')
        }

    def is_priv_message(self, event):
        try:
            if event['event'] == 'message':
                return True
            else:
                return False
        except KeyError:
            return False

    def is_list_message(self, event):
        try:
            if event['event'] == 'list':
                return True
            else:
                return False
        except KeyError:
            return False

    def is_join_message(self, event):
        try:
            if event['event'] == 'join':
                return True
            else:
                return False
        except KeyError:
            return False

    def is_part(self, event):
        try:
            if event['event'] == 'part':
                return True
            else:
                return False
        except KeyError:
            return False

    def is_mode_message(self, event):
        try:
            if event['event'] == 'mode':
                return True
            else:
                return False
        except KeyError:
            return False

    def check_login_status(self, data):
        if re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data):
            return False
        else:
            return True

    def send_message(self, channel, message):
        self.sock.send('PRIVMSG %s :%s\n' % (channel, message.encode('utf-8')))

    def get_irc_socket_object(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        self.sock = sock

        try:
            sock.connect((self.config['server'], self.config['port']))
        except:
            print_bot_status_message('Cannot connect to server (%s:%s).' %
                                     (self.config['server'], self.config['port']), 'error')
            sys.exit()

        sock.settimeout(None)

        sock.send('USER %s\r\n' % self.config['username'])
        sock.send('PASS %s\r\n' % self.config['oauth_password'])
        sock.send('NICK %s\r\n' % self.config['username'])

        if self.check_login_status(sock.recv(1024)):
            print_bot_status_message('Login successful.')
        else:
            print_bot_status_message(
                'Login unsuccessful. (hint: make sure your oauth token is set in config/config.py).', 'error')
            sys.exit()

        # start threads for channels that have cron messages to run
        for channel in self.config['channels']:
            if channel in self.config['cron']:
                if self.config['cron'][channel]['run_cron']:
                    channel = channel.lower()
                    thread.start_new_thread(cron.cron(self, channel).run, ())

        self.join_channels(self.channels_to_string(self.config['channels']))

        return sock

    def channels_to_string(self, channel_list):
        return ','.join(channel_list)

    def join_channels(self, channels):
        print_bot_status_message('Joining channels %s.' % channels)
        self.sock.send('JOIN %s\r\n' % channels)
        print_bot_status_message('Joined channels.')

    def leave_channels(self, channels):
        print_bot_status_message('Leaving chanels %s,' % channels)
        self.sock.send('PART %s\r\n' % channels)
        print_bot_status_message('Left channels.')