# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
"""

from typing import List, Union  # , Optional

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.wrappers import Response as FlaskResponse
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.sql.expression import Select
from werkzeug.wrappers.response import Response as WerkzeugResponse

# app imports
from codeapp import bcrypt, db
from codeapp.forms import (
    LoginForm,
    RegistrationForm,
    UpdatePasswordForm,
    UpdateProfileForm,
)
from codeapp.models import Recipe, User

Response = Union[str, FlaskResponse, WerkzeugResponse]

bp = Blueprint("bp", __name__, url_prefix="/")

"""
############################### General routes ################################

The routes below include general views open for all users.
"""


@bp.get("/")
def home() -> Response:
    statement: Select = select(Recipe).order_by(Recipe.date_posted)

    if "title" in request.args and len(request.args["title"]) > 0:
        # the user searched
        title: str = request.args["title"]
        flash(f"search the recipe by'{title}'.", "warning")
        statement = statement.filter(Recipe.title.like(f"%{title}%"))  # type: ignore

    recipes: List[Recipe] = db.session.execute(statement).scalars().all()
    return render_template("home.html", recipes=recipes)


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


"""
########################## Specific project routes ############################

Add here the routes specific to your project.
"""


@bp.get("/recipe/<int:recipe_id>")
def detail_recipe(recipe_id: int) -> Response:
    statement: Select = select(Recipe).filter_by(id=recipe_id)
    recipe: Recipe = db.session.execute(statement).scalars().one_or_none()
    if recipe is None:
        abort(404)
    return render_template("recipe.html", recipe=recipe)


"""
@bp.get("/delete_recipe/<int:recipe_id>")
@login_required
def delete_recipe(recipe_id: int) -> Response:
    # check if the recipe exists
    stmt: Select = select(Recipe).filter_by(id=recipe_id)
    recipe: Optional[Recipe] = db.session.execute(stmt).scalars().one_or_none()
    if recipe is None:  # the recipe with this id does not exist
        flash("This recipe does not exist!", "danger")
        return redirect(url_for("bp.home"))
    if recipe.user_id != current_user.id:  # the recipe does not belong to this user
        flash("This recipe does not belong to you!", "danger")
        return redirect(url_for("bp.home"))

    # if you get to this point, two things are known:
    # 1: the recipe exists
    # 2: the current_user is the owner of the recipe
    # now we can finally delete it
    try:
        db.session.delete(recipe)
        db.session.commit()
        flash("Recipe deleted successfully!", "success")
    except Exception as e:
        current_app.logger.exception(e)
        db.session.rollback()
        flash("Error while deleting recipe!", "danger")

    return redirect(url_for("bp.home"))
"""


"""
############################ User-related routes ##############################

The routes below include routes related to the user.
"""


@bp.route("/register", methods=["GET", "POST"])
def register() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for("bp.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        _password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        _user = User(name=form.name.data, email=form.email.data, password=_password)
        db.session.add(_user)
        try:
            db.session.commit()
            flash("User successfully created. Please log in!", "success")
            return redirect(url_for("bp.login"))
        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()
            flash(
                "There was an error while creating your user. Please try again later.",
                "danger",
            )
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for("bp.home"))
    form = LoginForm()
    if form.validate_on_submit():
        _stmt = select(User).filter(User.email == form.email.data).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        current_app.logger.debug(f"User ({type(_user)}): {_user}")
        if _user and bcrypt.check_password_hash(_user.password, form.password.data):
            login_user(_user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Welcome!", "success")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("bp.home"))
        flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@bp.get("/logout")
def logout() -> Response:
    logout_user()
    flash("Logout successful!", "success")
    return redirect(url_for("bp.login"))


@bp.get("/profile")
@login_required
def profile() -> Response:
    return render_template("profile.html")


@bp.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile() -> Response:
    profile_form = UpdateProfileForm()
    password_form = UpdatePasswordForm()

    if profile_form.validate_on_submit():
        current_app.logger.info("profile form submitted")
        _stmt = select(User).filter(User.id == current_user.id).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        _user.name = profile_form.name.data
        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
            current_app.logger.info("Profile updated successfully")
            return redirect(url_for("bp.profile"))
        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()
            flash(
                "There was an error while updating your profile. "
                "Please try again later.",
                "danger",
            )

    if password_form.validate_on_submit():
        # user tried to update its password
        # if it gets here, it's because the current password is validated
        # new password and confirmation are also equal
        # see forms.py for more info
        _new_password = bcrypt.generate_password_hash(
            password_form.new_password.data
        ).decode("utf-8")
        _stmt = select(User).filter(User.id == current_user.id).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        _user.password = _new_password
        try:
            db.session.commit()
            current_app.logger.info("Password changed successfully.")
            flash(
                "Password updated successfully! Log in with your new password!",
                "success",
            )
            logout_user()
            return redirect(url_for("bp.login"))
        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()
            flash(
                "There was an error while updating your password. "
                "Please try again later.",
                "danger",
            )

    # filling the form with the current data
    profile_form.name.data = current_user.name

    return render_template(
        "update_profile.html",
        profile_form=profile_form,
        password_form=password_form,
    )
