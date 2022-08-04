from __future__ import annotations

# python built-in imports
from dataclasses import dataclass, field
from datetime import datetime

# from mimetypes import init
from typing import List, Optional

# python external modules
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, select
from sqlalchemy.orm import registry, relationship

# app imports
from codeapp import db, login_manager

# import profile
# import string
# from cgitb import text


# from xml.etree.ElementTree import Comment


mapper_registry: registry = registry(metadata=db.metadata)


@login_manager.user_loader
def load_user(user_id: int) -> UserMixin:
    stmt = select(User).where(User.id == user_id).limit(1)
    return db.session.execute(stmt).scalars().first()


@mapper_registry.mapped
@dataclass
class User(UserMixin):
    __tablename__ = "user"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    name: str = field(
        repr=False,
        metadata={"sa": Column(String(128), nullable=False)},
    )
    email: str = field(
        metadata={"sa": Column(String(128), unique=True, nullable=False)}
    )
    password: str = field(
        repr=False, metadata={"sa": Column(String(128), nullable=False)}
    )

    # one-to-many relationship: one user can have zero, one or many recipes
    recipes: List[Recipe] = field(
        init=False,
        repr=False,
        metadata={
            "sa": relationship(
                "Recipe",
                back_populates="user",
                order_by="Recipe.date_posted",
            )
        },
    )

    # one-to-many relationship: one user can have zero, one or many comments
    comments: List[Comment] = field(
        init=False,
        repr=False,
        metadata={
            "sa": relationship(
                "Comment",
                back_populates="user",
                order_by="Comment.date_posted",
            )
        },
    )

    # one-to-many relationship: one user can have zero, one or many grades
    grades: List[Grade] = field(
        init=False,
        repr=False,
        metadata={
            "sa": relationship(
                "Grade",
                back_populates="user",
            )
        },
    )


@mapper_registry.mapped
@dataclass
class Recipe:
    __tablename__ = "recipe"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    title: str = field(
        metadata={"sa": Column(String(100), nullable=False)},
    )
    date_posted: datetime = field(
        init=False,  # this has a default value
        metadata={"sa": Column(DateTime(), nullable=False, default=datetime.now)},
    )
    content: str = field(
        metadata={"sa": Column(Text(), nullable=False)},
    )

    # one-to-many relationship: one recipe can have zero, one or many comments
    comments: List[Comment] = field(
        init=False,
        repr=False,
        metadata={
            "sa": relationship(
                "Comment",
                back_populates="recipe",
                order_by="Comment.date_posted",
            )
        },
    )

    # one-to-many relationship: one recipe can have zero, one or many grades
    grades: List[Grade] = field(
        init=False,
        repr=False,
        metadata={
            "sa": relationship(
                "Grade",
                back_populates="recipe",
            )
        },
    )

    # one-to-many relationship: one recipe only belongs to one user
    user: User = field(
        repr=False,
        metadata={"sa": relationship(User, back_populates="recipes", lazy="select")},
    )
    # optional last  else: crash
    user_id: Optional[int] = field(
        default=None,
        metadata={"sa": Column(Integer(), ForeignKey("user.id"), nullable=False)},
    )


@mapper_registry.mapped
@dataclass
class Comment:
    __tablename__ = "comment"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    content: str = field(
        repr=False,
        metadata={"sa": Column(Text(), nullable=False)},
    )
    date_posted: datetime = field(
        metadata={"sa": Column(DateTime(), nullable=False)},
    )
    # one-to-many relationship: one comment only belongs to one user
    user: User = field(
        repr=False,
        metadata={"sa": relationship(User, back_populates="comments", lazy="select")},
    )
    # one-to-many relationship: one comment only belongs to one recipe
    recipe: Recipe = field(
        repr=False,
        metadata={"sa": relationship(Recipe, back_populates="comments", lazy="select")},
    )
    # optional last  else: crash
    user_id: Optional[int] = field(
        default=None,
        metadata={"sa": Column(Integer(), ForeignKey("user.id"), nullable=False)},
    )
    recipe_id: Optional[int] = field(
        default=None,
        metadata={"sa": Column(Integer(), ForeignKey("recipe.id"), nullable=False)},
    )


@mapper_registry.mapped
@dataclass
class Grade:
    __tablename__ = "grade"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    score: int = field(
        metadata={"sa": Column(Integer())},
    )
    # one-to-many relationship: one grade only belongs to one user
    user: User = field(
        repr=False,
        metadata={"sa": relationship(User, back_populates="grades", lazy="select")},
    )
    # one-to-many relationship: one grade only belongs to one recipe
    recipe: Recipe = field(
        repr=False,
        metadata={"sa": relationship(Recipe, back_populates="grades", lazy="select")},
    )
    # optional last  else: crash
    user_id: Optional[int] = field(
        default=None,
        metadata={"sa": Column(Integer(), ForeignKey("user.id"), nullable=False)},
    )
    recipe_id: Optional[int] = field(
        default=None,
        metadata={"sa": Column(Integer(), ForeignKey("recipe.id"), nullable=False)},
    )
