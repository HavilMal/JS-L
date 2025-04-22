import logging
import sys

from run import run, cli

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda x: x.levelno <= logging.WARNING)
stdout_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.addFilter(lambda x: x.levelno >= logging.ERROR)
stderr_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)


if __name__ == "__main__":
    run()
    # cli()
