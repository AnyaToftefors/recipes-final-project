import logging

from flask import url_for

from .utils import TestCase

# from urllib import response


class TestSearch(TestCase):
    """
    This class must implement the test cases related to the search use case.
    Implement as many methods as needed to cover 100% of the code.
    """

    def test_render(self) -> None:
        """
        This test tests the rendering of the page, and the creation of the route.
        A code snippet is provided below.
        """
        # response = self.client.get(url_for("bp.<function name>"))
        # self.assert200(response)
        # self.assertTemplateUsed("<template name>.html")
        # self.assert_html(response)

        response1 = self.client.get(
            url_for("bp.home"),
        )
        self.assertTemplateUsed("home.html")
        self.assertIn("Search for recipes", response1.data.decode())
        self.assert_html(response1)

    def test_search(self) -> None:
        """
        Example of test method.
        Put below the code for the test.
        """
        # _ = self.client.get(
        #     url_for("bp.home"),
        # )
        response2 = self.client.get(
            url_for("bp.home", title="error"),
        )

        self.assertTemplateUsed("home.html")
        self.assertIn("Search for recipes", response2.data.decode())
        self.assert_html(response2)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
