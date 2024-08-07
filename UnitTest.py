import importlib
from unittest import TestCase
from unittest.mock import Mock, mock_open, patch
from _pytest.fixtures import fixture
from requests import Response
from Config.Auth.Token import Token_Headers
from Config.Auth.Token.Token_Headers import read_token, get_headers
from Config.Server.Server import get_server_url
from JiraApi.Common.JiraServer import JiraServer
from XrayApi.Common.Response import JiraResponse
from XrayApi.Cucumber import Import, Export
from XrayApi.Cucumber.Import import get_file_from_path
from XrayApi.TestRuns import get_defined_run_status


@fixture
def reload_headers():
    yield
    importlib.reload(Token_Headers)


@fixture
def reload_cucumber():
    yield
    importlib.reload(Export)
    importlib.reload(Import)


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

    class TestCucumberImport:

        def test_get_english_feat_from_path(self, reload_cucumber):
            feat = "#language:en\nFeature:"
            data_mock = mock_open(read_data=feat)
            with patch("XrayApi.Cucumber.Import.open", data_mock):
                assert isinstance(get_file_from_path("PATH"), list)

        def test_get_non_english_feat_from_path(self, reload_cucumber):
            feat = "#language:es\nCaracteristica:"
            data_mock = mock_open(read_data=feat)
            with patch("XrayApi.Cucumber.Import.open", data_mock):
                TestCase().assertRaises(ValueError, get_file_from_path, "PATH")

    class TestAbstractResponse:

        def test_generate_file_name_no_query(self):
            response = Mock(Response)
            headers = {"Content-Type": "None"}
            url = "https://server.url/rest/raven/1.0/export/test"
            raw_mock = Mock(url=url, headers=headers)
            response.configure_mock(status_code=200, raw=raw_mock, url=url)
            assert "server.url_1.0_export_test" == JiraResponse(response)._generate_file_name()

        def test_generate_file_name_query(self):
            response = Mock(Response)
            headers = {"Content-Type": "None"}
            url = "https://server.url/rest/raven/1.0/export/test?filter=1670"
            raw_mock = Mock(url=url, headers=headers)
            response.configure_mock(status_code=200, raw=raw_mock, url=url)
            assert "server.url_filter=1670" == JiraResponse(response)._generate_file_name()


class TestJiraApi:

    class TestJiraServer:

        def test_server_entry_exit(self):
            with JiraServer():
                pass
