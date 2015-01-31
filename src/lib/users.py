"""
Users class to maintain users who are in IRC
"""
import time


class Users():
    def __init__(self):
        self.user_dict = {}

    def channel_exists(self, channel):
        try:
            exists = self.user_dict[channel]['users']
            return True
        except KeyError:
            self.user_dict[channel] = {}
            self.user_dict[channel]['users'] = []
            return True

    def add_to_channel(self, username, channel):
        try:
            timestamp = time.time()
            # check if it exists
            exist = False
            for user_info in self.user_dict[channel]['users']:
                if user_info["username"] == username:
                    exist = True

            if not exist:
                self.user_dict[channel]['users'].append(
                    {'username': username, 'joined': timestamp, 'activity': timestamp, 'mod': False}
                )
        except KeyError:
            self.channel_exists(channel)
            self.add_to_channel(username, channel)

    def remove_from_channel(self, username, channel):
        self.user_dict[channel]['users'].pop(username, None)

    def mod_user(self, username, channel):
        found = False
        try:
            for user_info in self.user_dict[channel]['users']:
                if user_info['username'] == username:
                    user_info['mod'] = True
                    found = True
            if not found:
                self.add_to_channel(username, channel)
        except KeyError:
            self.add_to_channel(username, channel)
            self.mod_user(username, channel)

    def unmod_user(self, channel, username):
        found = False
        try:
            for user_info in self.user_dict[channel]['users']:
                if user_info['username'] == username:
                    user_info['mod'] = False
                    found = True
            if not found:
                self.add_to_channel(username, channel)
        except KeyError:
            self.add_to_channel(username, channel)
            self.mod_user(username, channel)

    def update(self, username, channel):
        timestamp = time.time()
        found = False
        try:
            for user_info in self.user_dict[channel]['users']:
                if user_info['username'] == username:
                    user_info['activity'] = timestamp
                    found = True
            if not found:
                self.add_to_channel(username, channel)
        except KeyError:
            self.add_to_channel(username, channel)
            self.update(username, channel)

    def add(self):
        pass

    def remove(self):
        pass

    def list(self):
        pass