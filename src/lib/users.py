"""
Users class to maintain users who are in IRC
"""
import time


class Users():
    def __init__(self):
        self.user_dict = {}

    def list_users(self, channel=None):
        if channel:
            return self.user_dict[channel]['users']
        return self.user_dict

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
        for d in self.user_dict[channel]['users']:
            if d['username'] == username:
                self.user_dict[channel]['users'].remove(d)
                return True
        return False

    def update_mod_status(self, username, channel, status):
        found = False
        try:
            for user_info in self.user_dict[channel]['users']:
                if user_info['username'] == username:
                    user_info['mod'] = status
                    found = True
            if not found:
                self.add_to_channel(username, channel)
        except KeyError:
            self.add_to_channel(username, channel)
            self.update_mod_status(username, channel, status)

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
