from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, BigInteger, String
from database.engine import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    tg_id: Mapped[str] = mapped_column(BigInteger)

    role: Mapped[str] = mapped_column(String)

    name_pers_team: Mapped[str] = mapped_column(String)

    game_round: Mapped[int] = mapped_column(Integer)

    balance: Mapped[int] = mapped_column(Integer)

    gold: Mapped[int] = mapped_column(Integer)

    silver: Mapped[int] = mapped_column(Integer)

    platinum: Mapped[int] = mapped_column(Integer)

    palladium: Mapped[int] = mapped_column(Integer)

    cuprum: Mapped[int] = mapped_column(Integer)

    lithium: Mapped[int] = mapped_column(Integer)

    cobalt: Mapped[int] = mapped_column(Integer)

    rare_metals: Mapped[int] = mapped_column(Integer)

    iron: Mapped[int] = mapped_column(Integer)

    aluminium: Mapped[int] = mapped_column(Integer)