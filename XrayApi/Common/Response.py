import logging
from json import JSONDecodeError

from requests import Response


class JiraResponse:
    def __init__(self, response: Response) -> None:
        self.raw = response
        self.parsed = []
        self.log = logging.getLogger("JiraResponse")
        self._parse_status_code()
        self._parse_response()

    def _parse_response(self) -> None:
        try:
            self.parsed = self.raw.json()
        except JSONDecodeError as error:
            self.log.error(f"Decode error in pos {error.pos} in document {error.doc}")
            raise

        self.log.debug(f"Found {len(self.parsed)} resources in {self.raw.url}")
        for data in self.parsed:
            self.log.debug(f"Found resource {data}")
        self.log.info(f"Got response {self.parsed}")


    def _parse_status_code(self) -> None:
        code = int(self.raw.status_code)
        if code == 200:
            self.log.debug(f"Response status OK with {code}")
            return
        elif code == 400:
            msg = f"Bad_request in Response with {code} and error text '{self.raw.text}'"
        elif code == 401:
            msg = "Unauthorized licence'"
        elif code == 500:
            msg = "Internal Server error in Response'"
        else:
            msg = f"Error in Response with {code} and error text '{self.raw.text}'"
        self.log.error(msg)
        # TODO retrieve HTTPResponse data
        raise ValueError(msg)
