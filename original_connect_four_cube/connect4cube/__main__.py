import logging
import sys

from connect4cube.selector import Selector

LOG = logging.getLogger(__name__)
LOG.debug("sys.path=" + ":".join(sys.path))

if __name__ == "__main__":
    selector = Selector()
    while True:
        selector.run()
