from time import sleep

import requests


def with_url(url: str) -> None:
    number_of_tries = 0
    while number_of_tries < 30:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return
        except Exception:
            pass
        sleep(.5)
        number_of_tries += 1

