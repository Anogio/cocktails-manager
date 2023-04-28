from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Liquid(Enum):
    GIN = "Gin"
    RUM = "Rum"
    VODKA = "Vodka"
    CHARTREUSE = "Chartreuse"
    BRANDY = "Brandy"
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
    WALNUT_LIQUEUR = "Walnut Liqueur"
    HONEY_LIQUEUR = "Honey Liqueur"
    ANCHO_VERDE = "Ancho Verde Liqueur"
    MARASCHINO = "Maraschino"
    SHERRY = "Sherry"  # = Xeres
    CREME_DE_VIOLETTE = "Crème de Violette"
    AMARO = "Amaro"  # C'est du bitter, substituable Picon, Aperol, Campari
    GRAND_MARNIER = "Grand Marnier"
    GENTIANE = "Gentiane"
    ABSINTHE = "Absinthe"
    BENEDICTINE = "Bénédictine"
    GINGERBREAD_SYRUP = "Gingerbread Syrup"
    KAHLUA = "Kahlua"
    CHERRY_BRANDY = "Cherry brandy"
    TOMATO_JUICE = "Tomato juice"
    CACHACA = "Cachaça"
    CALVADOS = "Calvados"
    LILLET_BLONDE = "Lillet blonde"


class Method(Enum):
    STIR = "Stir and strain"
    SHAKE = "Shake and strain"
    BUILD = "Build"


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


class CustomCategory(Enum):
    UNKNOWN = "Unknown"
    WANT_TO_TRY = "Want to try"
    FAVORITE = "Favorite"
    TRIED_NOT_FAVORITE = "Tried"
    CLASSIC = "Classic"


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
    name: str
    doses: list[Dose]
    family: Family
    method: Optional[Method]
    addons: Optional[list[str]] = None
    preparation_recommendation: str = ""
    feedback: str = ""
    custom_category: CustomCategory = CustomCategory.UNKNOWN

    def to_json(self):
        return {
            "name": self.name,
            "doses": [d.to_json() for d in self.doses],
            "family": self.family.value,
            "method": self.method.value,
            "addons": self.addons,
            "preparation_recommendation": self.preparation_recommendation,
            "feedback": self.feedback,
            "custom_category": self.custom_category.value
            if self.custom_category != CustomCategory.UNKNOWN
            else None,
        }

    def __str__(self):
        ingredients = "\n".join(
            [f"    {dose.alcohol.value}: {dose.quantity_ounces}" for dose in self.doses]
        )
        return f"""
<h3><b>{self.name}</b> ({self.family.value}) {(' - ' + self.custom_category.value) if self.custom_category != CustomCategory.UNKNOWN else ''}</h3>
<b>Ingredients</b>:
{ingredients}
    {", ".join(self.addons) if self.addons is not None else ""}

<b>Preparation</b>: {self.method.value}. {self.preparation_recommendation}
{ "<b>Feedback</b>: " + self.feedback if self.feedback else ""}
"""
