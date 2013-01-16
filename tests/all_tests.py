import sys
import os

# add parent dir to sys.path
lib_dir = os.path.abspath(os.path.join(__file__, '../..'))
sys.path.append(lib_dir)

# configure logging for tests
import logging
logging.basicConfig()


