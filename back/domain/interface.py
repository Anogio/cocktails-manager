from db.db_connector import DbConnector
from domain.cocktail_utils import cocktail_score
from domain.entitites import Cocktail, Liquid
from domain.substitutions import get_substituted_ingredient_list


def get_cocktails_for_ingredients(
    available_ingredients: list[Liquid],
    susbstitute: bool,
) -> tuple[list[Cocktail], list[Liquid], dict[Liquid, int]]:
    cocktails = DbConnector().get_all_cocktails()
    counts = DbConnector().get_cocktail_count_by_ingredient()

    if len(available_ingredients) == 0:
        possible_cocktails = sorted(cocktails, key=lambda c: c.name)
        available_ingredients = available_ingredients
    else:
        available_ingredients = set(available_ingredients)
        if susbstitute:
            available_ingredients = get_substituted_ingredient_list(
                available_ingredients
            )

        scored_cocktails = [
            (cocktail, cocktail_score(cocktail, available_ingredients, counts))
            for cocktail in cocktails
        ]
        possible_cocktails = sorted(
            [(cocktail, score) for cocktail, score in scored_cocktails if score > 0],
            key=lambda cocktail_score: cocktail_score[1],
            reverse=True,
        )
        possible_cocktails = [cocktail for cocktail, _ in possible_cocktails]
    return possible_cocktails, list(available_ingredients), counts
