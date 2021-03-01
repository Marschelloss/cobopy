import argparse
import sys

from logzero import logger, loglevel
from os import getenv
from cobopy import helper


__author__ = "Marcel Keßler"
__version__ = "0.1.0"


def main(args):
    # Disable verbose logging if no '-v' flag.
    if args.verbose == 0:
        loglevel(20)
    logger.debug("Provided arguments: %s" % args)

    env = {
        'BOT_ID': getenv('BOT_ID'),
        'BOT_TOKEN': getenv('BOT_TOKEN'),
        'CHAT_ID': getenv('CHAT_ID'),
        'SQLITE_DB': getenv('SQLITE_DB')
    }
    for e in env:
        if env[e] is None:
            logger.error("Environment Variable '%s' cannot be empty!" % e)
            sys.exit()

    helper.setup_db()

    logger.info("Starting cobopy...")

    # Late import so Class __init__ in helper.py doesn't fail
    from cobopy import catcher
    catcher.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
