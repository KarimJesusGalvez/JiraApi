import importlib
from unittest.mock import Mock

from _pytest.fixtures import fixture

from Config.Auth.Token import Token_Headers
from Config.Auth.Token.Token_Headers import read_token, get_headers

@fixture
def reload():
    yield
    importlib.reload(Token_Headers)

class TestAuth:

    def test_auth_file(self):
        result = read_token()
        if len(result) != 44:
            raise AssertionError("Token length")

    def test_get_headers(self, reload):
        result = get_headers()
        Token_Headers.read_token = Mock(return_value="AA")
        assert "Authorization" in result
        assert "Accept" in  result