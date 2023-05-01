from collections import defaultdict
from typing import Optional

from sqlalchemy import create_engine, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from db.models import Cocktail, CocktailDose, CocktailUserData
from domain.entitites import Cocktail as DomainCocktail
from domain.entitites import Dose, Family, FavoriteStatus, Liquid, Method

CONNECTION_STRING = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)
engine = create_engine(CONNECTION_STRING)

Session = sessionmaker()
Session.configure(bind=engine)


class DbConnector:
    @staticmethod
    def create_cocktail(cocktail: DomainCocktail) -> int:
        db_cocktail = Cocktail(
            name=cocktail.name,
            method=cocktail.method.name,
            family=cocktail.family.name,
            addons=cocktail.addons,
            instructions=cocktail.preparation_recommendation,
            doses=[
                CocktailDose(
                    quantity_ounces=dose.quantity_ounces, liquid=dose.alcohol.name
                )
                for dose in cocktail.doses
            ],
        )
        with Session() as session:
            session.add(db_cocktail)
            session.commit()
            assert db_cocktail.id
            return db_cocktail.id

    @staticmethod
    def set_cocktail_favorite_status(
        cocktail_id: int, favorite_status: FavoriteStatus
    ) -> None:
        with Session() as session:
            statement = insert(CocktailUserData).values(
                cocktail_id=cocktail_id, favorite_status=favorite_status.name
            )
            statement = statement.on_conflict_do_update(
                index_elements=[CocktailUserData.cocktail_id],
                set_={
                    CocktailUserData.favorite_status: statement.excluded.favorite_status
                },
            )
            session.execute(statement)
            session.commit()

    @staticmethod
    def set_cocktail_feedback(cocktail_id: int, feedback: str) -> None:
        with Session() as session:
            statement = insert(CocktailUserData).values(
                cocktail_id=cocktail_id, feedback=feedback
            )
            statement = statement.on_conflict_do_update(
                index_elements=[CocktailUserData.cocktail_id],
                set_={CocktailUserData.feedback: statement.excluded.feedback},
            )
            session.execute(statement)
            session.commit()

    @staticmethod
    def _domain_cocktail_from_db(
        cocktail: Cocktail,
        doses: list[CocktailDose],
        user_data: Optional[CocktailUserData],
    ) -> DomainCocktail:
        return DomainCocktail(
            cocktail_id=cocktail.id,
            name=cocktail.name,
            doses=[
                Dose(alcohol=Liquid[dose.liquid], quantity_ounces=dose.quantity_ounces)
                for dose in doses
            ],
            family=Family[cocktail.family],
            method=Method[cocktail.method],
            addons=cocktail.addons,
            preparation_recommendation=cocktail.instructions,
            feedback=user_data.feedback if user_data is not None else None,
            favorite_status=FavoriteStatus[user_data.favorite_status]
            if (user_data is not None and user_data.favorite_status is not None)
            else FavoriteStatus.NONE,
        )

    def get_cocktail_by_id(self, cocktail_id: int) -> DomainCocktail:
        with Session() as session:
            db_cocktail = (
                session.query(Cocktail).filter(Cocktail.id == cocktail_id).one()
            )
            return self._domain_cocktail_from_db(
                cocktail=db_cocktail,
                doses=db_cocktail.doses,
                user_data=db_cocktail.user_data,
            )

    def get_all_cocktails(self) -> list[DomainCocktail]:
        with Session() as session:
            db_cocktails = session.query(Cocktail).all()

            db_doses = session.query(CocktailDose).all()
            doses_by_cocktail = defaultdict(list)
            for dose in db_doses:
                doses_by_cocktail[dose.cocktail_id].append(dose)

            db_user_data = session.query(CocktailUserData).all()
            user_data_by_cocktail = {
                user_data.cocktail_id: user_data for user_data in db_user_data
            }

            return [
                self._domain_cocktail_from_db(
                    cocktail=cocktail,
                    doses=doses_by_cocktail[cocktail.id],
                    user_data=user_data_by_cocktail.get(cocktail.id),
                )
                for cocktail in db_cocktails
            ]

    @staticmethod
    def get_cocktail_count_by_ingredient() -> dict[Liquid, int]:
        with Session() as session:
            counts = (
                session.query(CocktailDose.liquid, func.count(CocktailDose.cocktail_id))
                .group_by(CocktailDose.liquid)
                .all()
            )
            return {Liquid[l]: c for (l, c) in counts}
