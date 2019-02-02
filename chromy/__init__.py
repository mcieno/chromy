# -*- coding: utf-8 -*-
import os
import pandas
import selenium
import sys
import time

from .chromy import *

try:
    from console_logging.console import Console
    log = Console()
    log.timeless()

except ImportError:
    import logging
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)-8s] : %(message)s')
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    log = logging.getLogger()
    log.removeHandler(log.handlers[0])
    log.addHandler(handler)
    # Aliasing function names
    log.log = log.info
    log.success = log.info
    log.warning = log.debug

from selenium.common.exceptions import *
from selenium.webdriver import *
from selenium.webdriver.common.action_chains import *
from selenium.webdriver.common.by import *
from selenium.webdriver.common.keys import *
from selenium.webdriver.support import *
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.ui import *

# Promote these modules, so that ``from chromy import *`` will let you access them

pd = pandas
EC = selenium.webdriver.support.expected_conditions
