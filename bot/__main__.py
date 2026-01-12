# core imports
from loguru import logger

# custom imports
from util import cfg
from util.models import BouncerBot
from util.handlers.logging import LogHandler


LogHandler.init_logging()


def main():
    bot = BouncerBot()

    bot.run(cfg.bot.token, log_handler=None)

    logger.info(
        "# ---------------------------------------------------------------------------- #"
    )
    logger.info(
        "#                             BOT SHUTDOWN COMPLETE                            #"
    )
    logger.info(
        "# ---------------------------------------------------------------------------- #"
    )


if __name__ == "__main__":
    main()
