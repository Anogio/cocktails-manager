from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Optional

from domain.interface import get_cocktails_for_ingredients, get_cocktail_counts_by_ingredient
from domain.cocktails import cocktails

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://cocktails-manager.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/cocktails")
def get_cocktails(ingredients: Annotated[Optional[list[str]], Query()] = None, substitute: bool = False):
    ingredients = ingredients if ingredients is not None else []
    cocktails = get_cocktails_for_ingredients(available_ingredients=ingredients, susbstitute=substitute)
    counts = sorted(get_cocktail_counts_by_ingredient().items(), key=lambda x: (-x[1], x[0].value))
    return {
        "cocktails": [{**c.to_json(), "index": i} for c, i in cocktails],
        "ingredients": [{
            "display_name": ingredient.value,
            "code": ingredient.name,
            "count": count
        } for ingredient, count in counts],
    }


@app.get("/cocktails/{index}")
def get_cocktail(index: int):
    return str(cocktails[index])
