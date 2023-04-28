from domain.data_model import Liquid, Cocktail
from domain.substitutions import get_substituted_ingredient_list
from domain.cocktails import cocktails
from domain.cocktail_utils import cocktail_score, get_cocktail_counts_by_ingredient


def get_cocktails_for_ingredients(
    available_ingredients: list[Liquid],
    susbstitute: bool,
) -> tuple[list[tuple[Cocktail, int]], list[Liquid]]:
    if len(available_ingredients) == 0:
        res = sorted(cocktails, key=lambda c: c.name)
        ingredients = available_ingredients
    else:
        ingredients = set(available_ingredients)
        if susbstitute:
            ingredients = get_substituted_ingredient_list(ingredients)

        possible_cocktails = [
            cocktail
            for cocktail in cocktails
            if cocktail_score(cocktail, ingredients) > 0
        ]
        res = sorted(
            possible_cocktails,
            key=lambda c: cocktail_score(c, ingredients),
            reverse=True,
        )

    return [(c, cocktails.index(c)) for c in res], list(ingredients)
