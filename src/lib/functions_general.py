import time

console_text_color_red = "\033[01;31m{0}\033[00m"
console_text_color_green = "\033[01;36m{0}\033[00m"
console_text_color_blue = "\033[01;34m{0}\033[00m"
console_text_color_cyan = "\033[01;36m{0}\033[00m"


def print_bot_status_message(message, status_type='INFO'):
    status_type = status_type.upper()

    if status_type == "ERROR":
        status_type = console_text_color_red.format(status_type)

    print '[%s] [%s] %s' % (time.strftime('%H:%M:%S', time.gmtime()), status_type, message)


def print_bot_message(message, channel=''):
    if channel:
        print '[%s %s] [%s] %s' % (time.strftime('%H:%M:%S', time.gmtime()), channel, 'BOT', message)
    else:
        print '[%s] [%s] %s' % (time.strftime('%H:%M:%S', time.gmtime()), 'BOT', message)
