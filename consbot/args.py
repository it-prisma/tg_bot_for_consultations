import argclass
from aiogram.enums import ParseMode
from aiomisc_log import LogFormat, LogLevel
from yarl import URL


class TelegramGroup(argclass.Group):
    bot_token: str = argclass.Argument(required=True, type=str, secret=True)
    parse_mode: ParseMode = argclass.Argument(
        type=ParseMode,
        choices=tuple(ParseMode._member_names_),
        default=ParseMode.HTML,
    )


class LoggingGroup(argclass.Group):
    level: LogLevel = argclass.Argument(
        choices=LogLevel.choices(), default=LogLevel.info, type=LogLevel
    )
    format: LogFormat = argclass.Argument(
        choices=LogFormat.choices(), default=LogFormat.color, type=LogFormat
    )


class PostgresqlGroup(argclass.Group):
    pg_dsn: URL = argclass.Argument(required=True)


class RedisGroup(argclass.Group):
    redis_dsn: URL = argclass.Argument(required=True)


class Parser(argclass.Parser):
    debug = argclass.Argument(action="store_true")
    pool_size = argclass.Argument(type=int, default=6, help="Thread pool size")

    telegram = TelegramGroup(title="Telegram options")
    logging = LoggingGroup(title="Logging options")
    postgres = PostgresqlGroup(title="PostgreSQL options")
    redis = RedisGroup(title="Redis options")


def get_parser() -> Parser:
    parser = Parser(auto_env_var_prefix="APP_")
    parser.parse_args()
    parser.sanitize_env()
    return parser
