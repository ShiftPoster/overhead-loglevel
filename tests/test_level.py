from argparse import ArgumentParser
from itertools import chain

import pytest

from overhead_loglevel import Level

try:
    import loguru  # type: ignore # noqa: F401

    LOGURU_INSTALLED: bool = True
except ImportError:
    LOGURU_INSTALLED: bool = False


@pytest.mark.skipif(
    not LOGURU_INSTALLED, reason="'loguru' needs to be installed for this test."
)
def test_loguru():
    assert Level.TRACE


@pytest.mark.skipif(
    LOGURU_INSTALLED, reason="'loguru' can't be installed for this test."
)
def test_no_loguru():
    assert not hasattr(Level, "TRACE")


def test_pydantic():
    pydantic = pytest.importorskip("pydantic")

    class Cls(pydantic.BaseModel):
        level: Level = Level.field()

    Cls(level=Level.WARN)


@pytest.mark.parametrize(
    "level",
    tuple(chain(Level, Level.__members__.keys(), map(str.lower, Level.__members__.keys()))),
)
def test_argparse(level: str | int | Level):
    parser = ArgumentParser()
    Level.add_argument(parser)
    args = parser.parse_args(("--log-level", str(level)))
    assert Level(args.log_level) == Level(level)


def test_basesettings(): ...
