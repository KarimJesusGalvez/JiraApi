import logging
from json import JSONDecodeError

from requests import Response


class JiraResponse:
    def __init__(self, response: Response) -> None:
        self.raw = response
        self.parsed = ""
        self.log = logging.getLogger("JiraResponse")
        self._parse_status_code()
        self._parse_response()

    def _parse_response(self) -> None:

        if "application/json" in self.raw.raw.headers["Content-Type"]:

            try:
                self.parsed = self.raw.json()
                self.log.debug(f"Found {len(self.parsed)} resources in {self.raw.url}")
                for data in self.parsed:
                    self.log.debug(f"Found resource {data}")
                self.log.info(f"Got response {self.parsed}")
            except JSONDecodeError as error:
                self.log.error(f"Decode error in pos {error.pos} in document {error.doc}")
                raise

        elif "application/octet-stream" in self.raw.raw.headers["Content-Type"]:
            self.log.debug(f"Found File data in {self.raw.url}")
            self.parsed = self.raw.text
            self._print_to_file()
        else:
            self.log.debug(f"Unrecognized response "
                           f"Content-Type {self.raw.raw.headers['Content-Type']} in {self.raw.url}")

    def _parse_status_code(self) -> None:
        code = int(self.raw.status_code)
        if code == 200:
            self.log.debug(f"Response status OK with {code}")
            return
        elif code == 400:
            msg = f"Bad_request in Response with {code} and error text '{self.raw.text}'"
        elif code == 401:
            msg = "Unauthorized licence'"
        elif code == 406:
            self.raw.request.headers["Authorization"] = "****"
            msg = f"Not Acceptable error in Request " \
                  f"\nURL:{self.raw.request.url}\nHeaders:{self.raw.request.headers}\nBody:{self.raw.request.body}'"
        elif code == 500:
            msg = "Internal Server error in Response'"
        else:
            msg = f"Error in Response with {code} and error text '{self.raw.text}'"
        self.log.error(msg)
        # TODO retrieve HTTPResponse data
        raise ValueError(msg)

    def _print_to_file(self) -> None:
        # TODO
        raise NotImplementedError("")