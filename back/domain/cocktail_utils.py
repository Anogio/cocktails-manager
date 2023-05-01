from domain.entitites import Cocktail, Liquid


def cocktail_score(
    cocktail: Cocktail,
    ingredients: set[Liquid],
    cocktail_counts_by_ingredient: dict[Liquid, int],
) -> float:
    required_ingredients = set(d.alcohol for d in cocktail.doses)

    required_ingredients_score = sum(
        1 / cocktail_counts_by_ingredient[i] for i in required_ingredients
    )
    present_ingredients_score = sum(
        1 / cocktail_counts_by_ingredient[i]
        for i in ingredients
        if i in required_ingredients
    )
    return present_ingredients_score / required_ingredients_score
