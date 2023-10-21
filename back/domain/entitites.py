from dataclasses import dataclass
from enum import Enum
from typing import Optional

# TODO: stop using enum names everywhere in the API, add translations in the front


class Liquid(Enum):
    GIN = "Gin"
    RUM_DARK = "Dark rum"
    RUM_LIGHT = "Light rum"
    VODKA = "Vodka"
    CHARTREUSE = "Chartreuse"
    BRANDY = "Brandy"
    TEQUILA = "Tequila"
    PISCO = "Pisco"
    JAGERMEISTER = "Jägermeister"
    CAMPARI = "Campari"
    SWEET_VERMOUTH = "Sweet Vermouth"
    DRY_VERMOUTH = "Dry Vermouth"
    WHISKEY = "Whiskey"
    ORANGE_BITTERS = "Orange Bitters"
    ANGOSTURA_BITTERS = "Angostura Bitters"
    CHAMPAGNE = "Champagne"
    PROSECCO = "Prosecco"
    PORTO = "Porto"
    APEROL = "Aperol"
    PASTIS = "Pastis"
    GINGER_ALE = "Ginger ale"
    GINGER_BEER = "Ginger beer"
    LEMON_JUICE = "Lemon Juice"
    LIME_JUICE = "Lime Juice"
    TRIPLE_SEC = "Triple Sec"
    BEER = "Beer"
    SIMPLE_SYRUP = "Simple Syrup"
    CREME_DE_CACAO = "Crème de Cacao"
    BAILEYS = "Baileys"
    WALNUT_LIQUEUR = "Walnut Liqueur"
    HONEY_LIQUEUR = "Honey Liqueur"
    ANCHO_VERDE = "Ancho Verde Liqueur"
    MARASCHINO = "Maraschino"
    SHERRY = "Sherry"  # = Xeres
    CREME_DE_VIOLETTE = "Crème de violette"
    CREME_DE_CASSIS = "Crème de cassis"
    CREME_DE_MENTHE = "Crème de menthe"
    AMARO = "Amaro"  # C'est du bitter, substituable Picon, Aperol, Campari
    FERNET_BRANCA = "Fernet Branca"
    GRAND_MARNIER = "Grand Marnier"
    GENTIANE = "Gentiane"
    ABSINTHE = "Absinthe"
    BENEDICTINE = "Bénédictine"
    GINGERBREAD_SYRUP = "Gingerbread Syrup"
    CINNAMON_SYRUP = "Cinnamon syrup"
    ORGEAT_SYRUP = "Orgeat syrup"
    GRENADINE = "Grenadine"
    KAHLUA = "Kahlua"
    CHERRY_BRANDY = "Cherry brandy"
    TOMATO_JUICE = "Tomato juice"
    WORCESTERSHIRE_SAUCE = "Worcestershire sauce"
    APPLE_JUICE = "Apple juice"
    ORANGE_JUICE = "Orange juice"
    GRAPEFRUIT_JUICE = "Grapefruit juice"
    PINEAPPLE_JUICE = "Pineapple juice"
    PASSIONFRUIT_JUICE = "Passionfruit juice"
    CRANBERRY_JUICE = "Cranberry juice"
    COCONUT_CREAM = "Coconut cream"
    CACHACA = "Cachaça"
    CALVADOS = "Calvados"
    LILLET_BLONDE = "Lillet blonde"


class Method(Enum):
    STIR = "Stir and strain"
    SHAKE = "Shake and strain"
    BUILD = "Build"
    BLEND = "Blend"
    MUDDLE = "Muddle"


class Family(Enum):
    DUOS_TRIOS = "Duo/trio"
    ORPHANS = "Orphan"
    HIGHBALLS = "Highball"
    FRENCH_ITALIAN = "French-Italian"
    SIMPLE_SOURS = "Simple sour"
    INTERNATIONAL_SOURS = "International Sour"
    NEW_ORLEANS_SOURS = "New Orleans Sour"
    ENHANCED_SOURS = "Enhanced sour"
    SPARKLING_SOURS = "Sparkling Sour"
    SNAPPERS = "Snapper"
    HOT_DRINKS = "Hot drink"
    CHAMPAGNE_COCKTAILS = "Champagne cocktail"
    PUNCHES = "Punch"
    TIKI = "Tiki"
    FROZEN_DRINKS = "Frozen drink"
    JULEPS = "Juleps"


class FavoriteStatus(Enum):
    NONE = "None"
    BOOKMARKED = "Want to try"
    FAVORITE = "Favorite"


@dataclass
class Dose:
    alcohol: Liquid
    quantity_ounces: Optional[float]

    def to_json(self):
        return {
            "liquid": {
                "code": self.alcohol.name,
                "display_name": self.alcohol.value,
            },
            "quantity": self.quantity_ounces,
        }


@dataclass
class Cocktail:
    cocktail_id: int
    name: str
    doses: list[Dose]
    family: Family
    method: Optional[Method]
    addons: Optional[list[str]] = None
    preparation_recommendation: str = ""
    feedback: Optional[str] = ""
    favorite_status: FavoriteStatus = FavoriteStatus.NONE

    def to_json(self):
        return {
            "id": self.cocktail_id,
            "name": self.name,
            "doses": [d.to_json() for d in self.doses],
            "family": self.family.value,
            "method": self.method.value,
            "shaken": self.method
            == Method.SHAKE,  # TODO: use codified enum values and drop this prop
            "addons": self.addons,
            "preparation_recommendation": self.preparation_recommendation,
            "feedback": self.feedback,
            "favorite_status": self.favorite_status.name,
        }
