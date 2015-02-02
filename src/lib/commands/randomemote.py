# coding: utf8
"""
Developed by Shane Engelman <me@5h4n3.com>
GitHub: <https://github.com/singlerider/lorenzotherobot>
"""

import random
import json


def randomemote(roboraj):
    filename = 'src/res/global_emotes.json'

    try:
        data = json.loads(file(filename, 'r').read())
    except:
        return 'Error reading %s.' % filename

    emote = random.choice(data.keys())

    return '%s = %s' % (emote, emote[:1] + '​'.decode('utf8') + emote[1:])
