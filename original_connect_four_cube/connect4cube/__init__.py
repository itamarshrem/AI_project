import logging

import coloredlogs

__version__ = '0.1.0'

coloredlogs.install(level=logging.DEBUG,
                    fmt='%(asctime)s,%(msecs)-3d [%(levelname)-7s] %(name)-30.30s - %(message)s',
                    datefmt='%H:%M:%S')
