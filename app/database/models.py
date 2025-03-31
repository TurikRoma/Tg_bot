import os
SQL_ALCHEMY = os.getenv("DATABASE_URL")


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String, Boolean, DateTime, Text, BigInteger
from datetime import datetime
import app.database.requests as rq

engine = create_async_engine(url=SQL_ALCHEMY)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User_info(Base):
    __tablename__ = 'users_info'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    user_name: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str] = mapped_column(String(80), default='-')
    bot_description: Mapped[str] = mapped_column(Text, default='-')
    bot_name: Mapped[str] = mapped_column(String(80), default='Бадди')
    user_age: Mapped[int] = mapped_column(default=0)
    user_sex: Mapped[str] = mapped_column(String(10), default='-') # 0 - man, 1 - women
    is_registered: Mapped[bool] = mapped_column(Boolean, default=False)
    tg_premium: Mapped[bool] = mapped_column(Boolean)
    sub: Mapped[bool] = mapped_column(Boolean, default=False)

class User_sub(Base):
    __tablename__ = 'users_sub'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sub: Mapped[str] = mapped_column(String(25))
    time_sub: Mapped[datetime] = mapped_column(DateTime)
    time_end: Mapped[datetime] = mapped_column(DateTime)

class User_messages(Base):
    __tablename__ = "users_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=False)
    user_name: Mapped[str] = mapped_column(String(100))
    is_trial: Mapped[bool] = mapped_column(Boolean)
    message: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    time_message: Mapped[datetime] = mapped_column(DateTime)
    time_answer: Mapped[datetime] = mapped_column(DateTime)

class User_log(Base):
    __tablename__ = 'users_logs'

    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(BigInteger)
    type_action:Mapped[str] = mapped_column(String(30))
    user_action:Mapped[str] = mapped_column(Text)
    time:Mapped[datetime] = mapped_column(DateTime)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)