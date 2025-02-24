import logging
import logging.config
import os
from functools import partial
from logging import Logger

# ConsoleHandlerのログフォーマッターとして何を使うか
CONSOLE_HANDLER_FORMATTER = "json"

log_level = os.getenv("LOG_LEVEL", "INFO")

LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(module)s %(lineno)d %(request)s %(response)s",
            "json_ensure_ascii": False,
        },
    },
    "handlers": {
        "console": {
            "level": log_level,
            "class": "logging.StreamHandler",
            "formatter": CONSOLE_HANDLER_FORMATTER,
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": log_level,
            "propagate": False,
        },
    },
}


def get_logger(name: str) -> Logger:
    """ロガー取得関数

    Args:
        name (str): ログを出力するモジュール名

    Returns:
        Logger: ロガーオブジェクト
    """
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(name)

    # logger.errorのときは常にexc_info=Trueに設定
    logger.error = partial(logger.error, exc_info=True)  # type: ignore
    return logger
