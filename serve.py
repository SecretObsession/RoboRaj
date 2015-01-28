#!/usr/bin/env python2

from src.bot import *
from src.config.config import *

# Start RoboRaj
bot = RoboRaj(config=config).run()