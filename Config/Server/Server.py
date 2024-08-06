from os import path


def get_server_url() -> str:
    with open(path.join(path.dirname(__file__), "ServerURL.txt"), "r") as file:
        return file.read()
