from contextlib import contextmanager
from datetime import datetime, timedelta
import locale
import random
import re
import threading
from typing import Generator

LOCALE_LOCK = threading.Lock()


@contextmanager
def setlocale(name: str) -> Generator:
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


# pylint: disable=R0911
def fix(line: str) -> str:
    match = re.search(r"{{random_future_date:(.*?)}}", line)
    if match:
        date = datetime.now()
        increase = random.randint(2, 20)
        future_date = date + timedelta(days=increase)
        if match.groups()[0] == "timestamp":
            return re.sub(r"{{random_future_date:\w+}}", str(int(future_date.timestamp())), line)
        if match.groups()[0] == "tivoli":
            with setlocale("nl_NL.UTF-8"):
                tivolies = (
                    f'"day": "{future_date.strftime("%a %-d")}", '
                    f'"month": "{future_date.strftime("%B")}", '
                    f'"year": "{future_date.strftime("%Y")}",'
                )
                return line.replace("{{random_future_date:tivoli}}", tivolies)
        if match.groups()[0] == "simplon-groningen":
            with setlocale("nl_NL.UTF-8"):
                return line.replace("{{random_future_date:simplon-groningen}}", future_date.strftime("%a %-d %B %Y"))
        if match.groups()[0] == "vera-groningen":
            with setlocale("nl_NL.UTF-8"):
                return line.replace("{{random_future_date:vera-groningen}}", future_date.strftime("%A %-d %B"))
        if match.groups()[0] == "neushoorn-leeuwarden":
            with setlocale("nl_NL.UTF-8"):
                return line.replace("{{random_future_date:neushoorn-leeuwarden}}", future_date.strftime("%A %-d %B"))
        return re.sub(r"{{random_future_date:.*?}}", future_date.strftime(match.groups()[0]), line)
    return line
