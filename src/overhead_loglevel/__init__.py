import logging
from argparse import Action, ArgumentParser
from collections.abc import Iterable
from enum import IntEnum
from typing import Any, Self

try:
    import loguru  # type: ignore # noqa: F401

    LOGURU_INSTALLED: bool = True
except ImportError:
    LOGURU_INSTALLED: bool = False

try:
    from pydantic import Field  # type: ignore
except ImportError:
    Field = None


class Level(IntEnum):
    CRITICAL = logging.CRITICAL = 50
    ERROR = logging.ERROR = 40
    WARNING = logging.WARNING = 30
    INFO = logging.INFO = 20
    DEBUG = logging.DEBUG = 10
    ALL = logging.NOTSET = 0

    if LOGURU_INSTALLED:
        TRACE = 5

    FATAL = CRITICAL
    WARN = WARNING
    DEFAULT = INFO

    def __init__(self, *_):
        if self.name not in self._value2member_map_:
            self._value2member_map_[self.name] = self
        if self.name.lower() not in self._value2member_map_:
            self._value2member_map_[self.name.lower()] = self
        if str(self.value) not in self._value2member_map_:
            self._value2member_map_[str(self.value)] = self

    @classmethod
    def add_argument(
        cls,
        parser: ArgumentParser,
        flags: Iterable[str] = ("-ll", "--log-level"),
        default: Any = DEFAULT,
        help: str | None = "",
        **kwargs,
    ) -> Action:
        return parser.add_argument(
            *flags,
            default=default,
            help=help,
            **kwargs,
        )

    @classmethod
    def field(cls, *args, **kwargs) -> Self:
        if Field is None:
            raise ImportError("Install pydantic to use this method.")
        return Field(*args, **kwargs)
