from typing import List

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

Base = declarative_base()


class CocktailDose(Base):
    __tablename__ = "cocktail_doses"

    cocktail_id = sa.Column(
        sa.Integer, sa.ForeignKey("cocktails.id"), primary_key=True, autoincrement=False
    )
    quantity_ounces = sa.Column(sa.Float, nullable=False)
    liquid = sa.Column(sa.Text, nullable=False, primary_key=True)


class CocktailUserData(Base):
    __tablename__ = "cocktail_user_data"

    cocktail_id = sa.Column(
        sa.Integer, sa.ForeignKey("cocktails.id"), primary_key=True, autoincrement=False
    )
    favorite_status = sa.Column(sa.Text)
    feedback = sa.Column(sa.Text)


class Cocktail(Base):
    __tablename__ = "cocktails"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    method = sa.Column(sa.Text, nullable=False)
    family = sa.Column(sa.Text, nullable=False)
    addons = sa.Column(sa.ARRAY(sa.Text))
    instructions = sa.Column(sa.Text)

    doses: Mapped[List["CocktailDose"]] = relationship()
    user_data: Mapped["CocktailUserData"] = relationship()
