import importlib
from unittest.mock import Mock
from _pytest.fixtures import fixture
from Config.Auth.Token import Token_Headers
from Config.Auth.Token.Token_Headers import read_token, get_headers
from Config.Server.Server import get_server_url
from XrayApi.TestRuns import get_defined_run_status


@fixture
def reload_headers():
    yield
    importlib.reload(Token_Headers)


class TestAuth:

    def test_auth_file(self):
        result = read_token()
        if len(result) != 44:
            raise AssertionError("Token length")

    def test_get_headers(self, reload_headers):
        result = get_headers()
        Token_Headers.read_token = Mock(return_value="AA")
        assert "Authorization" in result
        assert "Accept" in result

    def test_get_server_url(self, reload_headers):
        assert get_server_url()


class TestXray:

    class TestTestIssues:

        def test_get_defined_test_status(self):
            assert len(get_defined_run_status().parsed) > 1
