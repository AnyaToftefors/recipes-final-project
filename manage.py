# built-in imports
import random
from datetime import datetime, timedelta
from typing import List

# external imports
from flask.cli import FlaskGroup
from lorem_text import lorem

# internal imports
from codeapp import bcrypt, create_app, db
from codeapp.models import Comment, Grade, Recipe, User

app = create_app()
cli = FlaskGroup(create_app=create_app)  # type: ignore


@cli.command("initdb")  # type: ignore
def initdb() -> None:
    with app.app_context():
        db.drop_all()
        db.create_all()

        # let's first generate a few users
        users: List[User] = []

        pwd = bcrypt.generate_password_hash("testing").decode("utf-8")
        default_1 = User(
            name="Default User",
            email="default@chalmers.se",
            password=pwd,
        )
        users.append(default_1)

        default_2 = User(
            name="Normal User",
            email="normal@chalmers.se",
            password=pwd,
        )
        users.append(default_2)

        # add all users to the database
        db.session.add_all(users)

        # commit to make sure everything with users is working
        db.session.commit()

        # now, for each user, let's generate some recipes
        recipes: List[Recipe] = []

        for user in users:
            for _ in range(random.randint(5, 7)):  # each user gets 5-7 recipes
                # picking a random date for the recipe in the last 90 days
                date_posted = datetime.now() - timedelta(
                    days=random.randint(20, 90),
                    hours=random.randint(1, 23),
                    minutes=random.randint(1, 59),
                )
                content: str = ""
                # the content has 1-3 paragraphs
                for paragraph in lorem.paragraphs(random.randint(1, 3)).split("\n"):
                    content += "<p>" + paragraph + "</p>"
                recipe = Recipe(
                    # the title has 3-7 words
                    title=lorem.words(random.randint(3, 7)).capitalize(),
                    content=content,
                    user=user,
                )
                # we set the date afterwards because
                # we need to override the default value
                recipe.date_posted = date_posted
                recipes.append(recipe)

        # add all recipes to the database
        db.session.add_all(recipes)

        # commit to make sure everything is ok
        db.session.commit()

        comments: List[Comment] = []

        for user in users:
            for recipe in recipes:
                date_posted = datetime.now() - timedelta(
                    days=random.randint(1, 20),
                    hours=random.randint(1, 23),
                    minutes=random.randint(1, 59),
                )
                comment = Comment(
                    content=content,
                    recipe=recipe,
                    date_posted=date_posted,
                    user=user,
                )
                comments.append(comment)

        db.session.add_all(comments)

        db.session.commit()

        grades: List[Grade] = []

        for user in users:
            for recipe in recipes:
                grade = Grade(
                    score=random.randint(1, 5),
                    recipe=recipe,
                    user=user,
                )
                grades.append(grade)

        db.session.add_all(grades)

        db.session.commit()

        app.logger.info("Success!")


if __name__ == "__main__":
    cli()
