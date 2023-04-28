from collections import defaultdict

from domain.cocktails import cocktails
from domain.data_model import Cocktail, Liquid


def get_cocktail_counts_by_ingredient() -> dict[Liquid, int]:
    counts = defaultdict(int)
    for cocktail in cocktails:
        for dose in cocktail.doses:
            counts[dose.alcohol] += 1
    return counts


def cocktail_score(cocktail: Cocktail, ingredients: set[Liquid]) -> float:
    counts = get_cocktail_counts_by_ingredient()
    required_ingredients = set(d.alcohol for d in cocktail.doses)

    required_ingredients_score = sum(1 / counts[i] for i in required_ingredients)
    present_ingredients_score = sum(
        1 / counts[i] for i in ingredients if i in required_ingredients
    )
    return present_ingredients_score / required_ingredients_score
