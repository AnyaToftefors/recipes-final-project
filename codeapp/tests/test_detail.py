import logging

from flask import url_for
from sqlalchemy import desc, select
from sqlalchemy.sql.expression import Select, func

from codeapp import db
from codeapp.models import Recipe, User

from .test_user import TestUser
from .utils import TestCase


class TestDetail(TestCase):
    """
    This class must implement the test cases related to the detail use case.
    Implement as many methods as needed to cover 100% of the code.
    """

    def test_detail_render(self) -> None:
        """
        This test tests the rendering of the page, and the creation of the route.
        A code snippet is provided below.
        """
        # get one object from the database
        # you can adjust the filtering to get the object you want
        # remember to add the imports
        statement: Select = select(Recipe).order_by(func.random()).limit(1)
        one: Recipe = db.session.execute(statement).scalars().one()

        response = self.client.get(url_for("bp.detail_recipe", recipe_id=one.id))
        self.assert200(response)
        self.assertTemplateUsed("recipe.html")
        self.assert_html(response)

    def test_detail_recipe(self) -> None:
        """
        This test makes sure that the title and other recipe content
        is present in the page.
        """
        # get one object from the database
        # you can adjust the filtering to get the object you want
        # remember to add the imports
        statement: Select = select(Recipe).order_by(func.random()).limit(1)
        one: Recipe = db.session.execute(statement).scalars().one()

        response = self.client.get(url_for("bp.detail_recipe", recipe_id=one.id))
        self.assert200(response)
        self.assertTemplateUsed("recipe.html")
        self.assertIn(one.title, response.data.decode())
        self.assert_html(response)

    def test_detail_recipe_not_existent(self) -> None:
        """
        This test makes sure that if I try to access a recipe that
        does not exist, I'll get a "not found" back.
        """
        # get one object from the database
        # you can adjust the filtering to get the object you want
        # remember to add the imports
        statement: Select = select(Recipe).order_by(desc(Recipe.id)).limit(1)
        one: Recipe = db.session.execute(statement).scalars().one()

        response = self.client.get(url_for("bp.detail_recipe", recipe_id=one.id + 100))
        self.assert404(response)

    def test_detail_recipe_not_yours(self) -> None:
        """
        This test asserts that if you open a recipe that is not
        yours, you will not see the "delete" button.
        """
        # get user id
        stmt_user: Select = select(User).filter_by(email=TestUser.username)
        user: User = db.session.execute(stmt_user).scalars().one()

        # first, we log in
        response = self.client.post(
            url_for("bp.login"),
            data={"email": TestUser.username, "password": TestUser.password},
            follow_redirects=True,
        )

        # get a recipe that does not belong to this user
        stmt: Select = (
            select(Recipe)
            .filter(Recipe.user_id != user.id)
            .order_by(func.random())
            .limit(1)
        )
        recipe: Recipe = db.session.execute(stmt).scalars().one()

        # make the request
        response = self.client.get(url_for("bp.detail_recipe", recipe_id=recipe.id))
        self.assert200(response)
        self.assertTemplateUsed("recipe.html")
        self.assertIn(recipe.title, response.data.decode())
        self.assertNotIn(
            "Are you sure you want to delete this recipe with", response.data.decode()
        )
        self.assert_html(response)


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
