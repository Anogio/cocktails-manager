from domain.entitites import Liquid

INGREDIENT_SETS = [
    (Liquid.GIN, Liquid.VODKA),
    (Liquid.RUM_DARK, Liquid.RUM_LIGHT, Liquid.CACHACA),
    (Liquid.CHARTREUSE, Liquid.ABSINTHE, Liquid.BENEDICTINE, Liquid.GENTIANE),
    (Liquid.BRANDY, Liquid.CHERRY_BRANDY, Liquid.CALVADOS),
    (Liquid.TEQUILA,),
    (Liquid.PISCO,),
    (Liquid.JAGERMEISTER,),
    (Liquid.CAMPARI, Liquid.APEROL, Liquid.AMARO, Liquid.FERNET_BRANCA),
    (Liquid.SWEET_VERMOUTH, Liquid.DRY_VERMOUTH, Liquid.LILLET_BLONDE),
    (Liquid.WHISKEY,),
    (Liquid.ANGOSTURA_BITTERS, Liquid.ORANGE_BITTERS),
    (Liquid.CHAMPAGNE, Liquid.PROSECCO),
    (Liquid.PORTO,),
    (Liquid.PASTIS,),
    (Liquid.GINGER_ALE, Liquid.GINGER_BEER),
    (Liquid.LEMON_JUICE, Liquid.LIME_JUICE),
    (Liquid.TRIPLE_SEC, Liquid.GRAND_MARNIER),
    (Liquid.BEER,),
    (Liquid.SIMPLE_SYRUP, Liquid.GRENADINE, Liquid.ORGEAT_SYRUP),
    (
        Liquid.HONEY_LIQUEUR,
        Liquid.WALNUT_LIQUEUR,
        Liquid.CREME_DE_CACAO,
        Liquid.CREME_DE_VIOLETTE,
        Liquid.GINGERBREAD_SYRUP,
        Liquid.CINNAMON_SYRUP,
    ),
    (Liquid.WORCESTERSHIRE_SAUCE,),
    (Liquid.CREME_DE_CASSIS, Liquid.CREME_DE_MENTHE, Liquid.BAILEYS),
    (Liquid.ANCHO_VERDE,),
    (Liquid.MARASCHINO,),
    (Liquid.SHERRY,),
    (Liquid.KAHLUA,),
    (Liquid.TOMATO_JUICE,),
    (Liquid.COCONUT_CREAM,),
    (
        Liquid.APPLE_JUICE,
        Liquid.ORANGE_JUICE,
        Liquid.GRAPEFRUIT_JUICE,
        Liquid.PINEAPPLE_JUICE,
        Liquid.CRANBERRY_JUICE,
        Liquid.PASSIONFRUIT_JUICE,
    ),
]

all_ingredients: list[Liquid] = list(Liquid)
all_susbtitutions = [i for s in INGREDIENT_SETS for i in s]

substitution_mapping = {i: s for s in INGREDIENT_SETS for i in s}

# Check that all ingredients are mentioned exactly once
assert len(all_ingredients) == len(all_susbtitutions)
assert set(all_ingredients) == set(all_susbtitutions)


def get_substituted_ingredient_list(
    available_ingredients: set[Liquid],
) -> set[Liquid]:
    ingredients_with_substitution = set()
    for ingredient in available_ingredients:
        for substitute in substitution_mapping[ingredient]:
            ingredients_with_substitution.add(substitute)
    return ingredients_with_substitution
