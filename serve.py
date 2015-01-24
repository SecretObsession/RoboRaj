#!/usr/bin/env python2

from sys import argv
from src.bot import *
from src.config.config import *
import datetime

#Logger is run. RoboRaj is contained within
bot = Logger(config=config).run()