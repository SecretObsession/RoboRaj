import os
import glob

# This will import all command modules
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + '/*.py')]
