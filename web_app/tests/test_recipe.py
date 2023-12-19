"""test recipe route"""

from unittest.mock import patch
import pytest
from web_app.app import app
from .recipe_test_data import TEST_REC


@pytest.fixture(name="client")
def fix_client():
    """web app test client"""
    app.config["TESTING"] = True
    with patch(
        "web_app.app.fetch_spoon_api",
        return_value="please patch me... don't waste API calls!",
    ):
        yield app.test_client()


class TestRecipe:
    """test suite"""

    def test_recipe_details(self, client):
        """test normal recipe page"""
        with patch("web_app.app.fetch_spoon_api", return_value=TEST_REC):
            res = client.get("/recipe/1234")
            assert res.status_code == 200

    def test_missing_nutrients(self, client):
        """test mutrition missing nutrients"""
        test_rec_m = TEST_REC
        test_rec_m["nutrition"]["nutrients"] = []
        with patch("web_app.app.fetch_spoon_api", return_value=test_rec_m):
            res = client.get("/recipe/1234")
            assert res.status_code == 200
