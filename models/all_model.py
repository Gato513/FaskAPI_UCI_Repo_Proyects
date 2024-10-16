from sqlalchemy import Column, Integer, String
from config.database_config import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    userphone = Column(String(20), nullable=False, unique=True)
    userdocument = Column(String(20), nullable=False, unique=True)
    useraddress = Column(String(100), nullable=False)
    usermatricula = Column(String(100), nullable=False)
    useremail = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    role = Column(String(5), nullable=False)

