import datetime

from sqlalchemy import Column, BigInteger, DateTime, Boolean, String

from app.db.base_class import Base


class Users(Base):
    id = Column(BigInteger, primary_key=True)

    username = Column(String)
    fullname = Column(String)
    is_admin = Column(Boolean, default=False)
    locale = Column(String, default="en")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
