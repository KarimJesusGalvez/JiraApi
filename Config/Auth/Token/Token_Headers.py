import logging
from os import path

log = logging.getLogger("Auth.Token")

def read_token() -> str:
    with open(path.join(path.dirname(__file__), "token.txt"), "r") as file:
        return file.read()


def get_headers() -> dict[str, str]:
    headers = {}
    headers["Authorization"] = f"Bearer {read_token()}"
    headers["Accept"] = "application/json"
    return headers
