global config

#
# IRC Bot example configuration
#

config = {
    # details required to login to twitch IRC server
    'server': 'irc.twitch.tv',  # twitch IRC server
    'port': 6667,
    'username': 'twitch_username',
    'oauth_password': 'oauth:',  # get this from http://twitchapps.com/tmi/
    'channels': ['#channel_one', '#channel_two'],  # channel to join, this must be lowercase
    'debug': False,  # if set to true will display any data received

    'cron':
    {
        '#channel_one':
        {
            'run_cron': False,  # set this to False if you want don't want to run the cronjob
            'run_time': 5,  # time in seconds
            'cron_messages': [
                'This is channel_one cron message one.',
                'This is channel_one cron message two.'
            ]
        },
        '#channel_two':
        {
            'run_cron': False,
            'run_time': 20,
            'cron_messages': [
                'This is channel_two cron message one.'
            ]
        }
    },
    'log_messages': True,  # set to true to log messages to file
    'socket_buffer_size': 2048  # maximum amount of bytes to receive from socket - 1024-4096 recommended
}

