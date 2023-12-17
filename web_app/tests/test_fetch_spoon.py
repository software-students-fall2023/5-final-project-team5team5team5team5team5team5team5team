import pytest
from unittest.mock import patch, Mock
from web_app.app import fetch_spoon_api

class mockresponse():
        def __init__(self, status):
            self.url = ''
            self.json = lambda: {'ok': 'ok'}
            self.status_code = status


class TestFetchSpoon():

    def test_build_url_empty_query(self):
        """test properly building api call with secret"""

        def testparams(path, params, timeout=-1):
            assert timeout > 0
            assert path == "https://test.nowaythisexists/"
            assert params == {"apiKey": "SECRET12345"}
            return mockresponse(200)

        with patch("web_app.app.SPOON_SECRET", "SECRET12345"), patch("requests.get", testparams):
            assert fetch_spoon_api('https://test.nowaythisexists/') == {'ok': 'ok'}

    def test_build_url_with_query(self):
        """test properly building api call with secret"""

        def testparams(path, params, timeout=-1):
            assert timeout > 0
            assert path == "https://test.nowaythisexists/"
            assert params == {"food": "id", "apiKey": "SECRET12345"}
            return mockresponse(429)

        with patch("web_app.app.SPOON_SECRET", "SECRET12345"), patch("requests.get", testparams):
            assert fetch_spoon_api('https://test.nowaythisexists/', {'food': 'id'}) is None
