"""
Command to see how many followers the channel's broadcaster has

Developed by Mike Herold <archangel.herold@gmail.com>
GitHub: <https://github.com/secretobsession/twitch-bot>
"""
from src.lib.twitch import Twitch


def followers(robo_info):
    channel = robo_info['command_info']['channel'].lstrip('#')
    twitch_class = robo_info['TwitchAPI']
    channel_info = twitch_class.fetch_channel_info(channel)
    return "This channel has %s followers!" % (channel_info["followers"],)