"""test fetch spoon api helper function"""

from collections import namedtuple
from unittest.mock import patch
from web_app.app import fetch_spoon_api


MockResponse = namedtuple("MockResponse", ["url", "json", "status_code"])


def get_mock_response(status):
    """mock response with status"""
    return MockResponse("", lambda: {"ok": "ok"}, status)


class TestFetchSpoon:
    """test suite"""

    def test_build_url_empty_query(self):
        """test properly building api call with secret"""

        def testparams(path, params, timeout=-1):
            assert timeout > 0
            assert path == "https://test.nowaythisexists/"
            assert params == {"apiKey": "SECRET12345"}
            return get_mock_response(200)

        with patch("web_app.app.SPOON_SECRET", "SECRET12345"), patch(
            "requests.get", testparams
        ):
            assert fetch_spoon_api("https://test.nowaythisexists/") == {"ok": "ok"}

    def test_build_url_with_query(self):
        """test properly building api call with secret"""

        def testparams(path, params, timeout=-1):
            assert timeout > 0
            assert path == "https://test.nowaythisexists/"
            assert params == {"food": "id", "apiKey": "SECRET12345"}
            return get_mock_response(429)

        with patch("web_app.app.SPOON_SECRET", "SECRET12345"), patch(
            "requests.get", testparams
        ):
            assert (
                fetch_spoon_api("https://test.nowaythisexists/", {"food": "id"}) is None
            )
