"""
 Twitch API for fetching Twitch Data
"""
import json
import urllib2


class Twitch():
    def __init__(self):
        self.user = self.User()
        self.channel = self.Channel()

    def fetch_user_info(self, username):
        return self.user.fetch_details(username)

    def fetch_channel_info(self, channel):
        return self.channel.fetch_details(channel)

    def fetch_channel_teams(self, channel):
        return self.channel.fetch_teams(channel)

    class User():
        def __init__(self):
            pass

        def fetch_details(self, username):
            request = urllib2.Request('https://api.twitch.tv/kraken/users/%s' % (username,))
            response = urllib2.urlopen(request).read()
            return json.loads(response)

    class Channel():
        def __init__(self):
            pass

        def fetch_details(self, channel):
            request = urllib2.Request('https://api.twitch.tv/kraken/channels/%s' % (channel,))
            response = urllib2.urlopen(request).read()
            return json.loads(response)

        def fetch_teams(self, channel):
            request = urllib2.Request('https://api.twitch.tv/kraken/channels/%s/teams' % (channel,))
            response = urllib2.urlopen(request).read()
            return json.loads(response)
