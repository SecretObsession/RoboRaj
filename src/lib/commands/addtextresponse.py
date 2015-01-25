"""
Add Text Response

Written by Mike Herold <archangel.herold@gmail.com> <github.com/SecretObsession/>
"""

# The list of commands needs to be imported so it can be updated to include the new command
def addtextresponse(args, commands):
    usage = '!addtextresponse <command> <message>'

    command = args[0]
    # set a hardcoded limit because of having to deal with large strings and potential for quotes
    command_cooldown = 10
    response_message = ""

    for argindex in range(1, len(args)):
        response_message += " %s" % (args[argindex])

    new_command = {
        'limit': command_cooldown,
        'return': response_message.lstrip()
    }

    # add the new command to the available commands list
    new_command_key = "!"+command
    commands[new_command_key] = new_command

    return "Added command as an available command"
