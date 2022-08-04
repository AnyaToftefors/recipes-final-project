import logging

from flask import url_for

from .utils import TestCase


class TestHomePage(TestCase):
    def test_home_page(self) -> None:
        response = self.client.get(url_for("bp.home"))
        self.assert200(response)
        self.assertTemplateUsed("home.html")
        self.assertIn("List of recipes", response.data.decode())
        self.assertIn("Title", response.data.decode())
        self.assertIn("Date", response.data.decode())
        self.assertIn("User", response.data.decode())
        self.assertIn("Content", response.data.decode())

        self.assert_html(response)

    def test_about_page(self) -> None:
        response = self.client.get(url_for("bp.about"))
        self.assert200(response)
        self.assertTemplateUsed("about.html")
        self.assertIn("About", response.data.decode())
        self.assert_html(response)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
