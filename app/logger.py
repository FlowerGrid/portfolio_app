import logging
import sys

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Avoid adding handlers multiple times (important with app factory)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        ">>> %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.propagate = False
