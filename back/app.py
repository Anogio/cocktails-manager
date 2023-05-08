from typing import Annotated, Optional

from db.db_connector import DbConnector
from domain.entitites import FavoriteStatus, Liquid
from domain.interface import get_cocktails_for_ingredients
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://cocktails-manager.anog.fr",
    "https://www.cocktails-manager.anog.fr",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/cocktails")
def get_cocktails(
    ingredients: Annotated[Optional[list[str]], Query()] = None,
    substitute: bool = False,
):
    available_ingredients = (
        [Liquid[s] for s in ingredients] if ingredients is not None else []
    )
    (
        possible_cocktails,
        ingredients_with_substitution,
        counts,
    ) = get_cocktails_for_ingredients(
        available_ingredients=available_ingredients, susbstitute=substitute
    )
    counts = sorted(counts.items(), key=lambda x: (-x[1], x[0].value))
    return {
        "cocktails": [c.to_json() for c in possible_cocktails],
        "ingredients": [
            {"display_name": ingredient.value, "code": ingredient.name, "count": count}
            for ingredient, count in counts
        ],
        "ingredients_with_substitution": [
            {"code": ingredient.name} for ingredient in ingredients_with_substitution
        ],
    }


@app.get("/cocktails/{index}")
def get_cocktail(index: int):
    return DbConnector().get_cocktail_by_id(index).to_json()


class UserDataInput(BaseModel):
    feedback: Optional[str] = None
    favorite_status: Optional[str] = None


@app.patch("/cocktails/{index}")
def update_cocktail_user_data(index: int, user_data: UserDataInput):
    """
    For now, only
    """
    if user_data.feedback is not None:
        DbConnector().set_cocktail_feedback(
            cocktail_id=index, feedback=user_data.feedback
        )

    if user_data.favorite_status is not None:
        DbConnector().set_cocktail_favorite_status(
            cocktail_id=index, favorite_status=FavoriteStatus[user_data.favorite_status]
        )

    return DbConnector().get_cocktail_by_id(cocktail_id=index).to_json()
