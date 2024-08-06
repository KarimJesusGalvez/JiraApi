import logging
from requests import Response


class JiraResponse:
    def __init__(self, response: Response) -> None:
        self.raw = response
        self.parsed = []
        self.log = logging.getLogger("JiraResponse")
        self._parse_status_code()
        self._parse_response()

    def _parse_response(self) -> None:
        self.parsed = self.raw.json()
        self.log.debug(f"Found {len(self.parsed)} resources in {self.raw.url}")
        for data in self.parsed:
            self.log.debug(f"Found resource {data}")
        self.log.info(f"Got response {self.parsed}")


    def _parse_status_code(self) -> None:
        code = int(self.raw.status_code)
        if 200 <= code < 300:
            self.log.debug(f"Response status OK with {code}")
        else:
            msg = f"Error in Response with {code} and error text '{self.raw.text}'"
            self.log.error(msg)
            # TODO retrieve HTTPResponse data
            raise ValueError(msg)
