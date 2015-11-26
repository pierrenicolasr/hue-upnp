import logging
import logging.handlers
import sys
from debug import DEBUG

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
L = logging.getLogger()
if DEBUG:
        L.setLevel(logging.DEBUG)
else:
        L.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
L.addHandler(consoleHandler)
