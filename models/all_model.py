from sqlalchemy import Column, Integer, String, Boolean,  ForeignKey
from sqlalchemy.orm import relationship
from config.database_config import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String(50), nullable=False, unique=True)
    user_phone = Column(String(20), nullable=False, unique=True)
    user_document = Column(String(20), nullable=False, unique=True)
    user_address = Column(String(100), nullable=False)
    user_matricula = Column(String(100), nullable=False)
    user_email = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    role = Column(String(5), nullable=False)

class Facultad(Base):
    __tablename__ = "facultad"
    id_facultad = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_facultad = Column(String(255), nullable=False)
    is_activated = Column(Boolean(), nullable=False, default=True)  #@ Trabajando
    carreras = relationship("Carrera", back_populates="facultad")

class Carrera(Base):
    __tablename__ = "carreras"
    id_carrera = Column(Integer, primary_key=True, index=True)
    nombre_carrera = Column(String(255), index=True)
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"))
    facultad = relationship("Facultad", back_populates="carreras")
    cursos = relationship("Curso", back_populates="carrera")

class Curso(Base):
    __tablename__ = "cursos"
    id_curso = Column(Integer, primary_key=True, index=True)
    nombre_curso = Column(String(255), index=True)
    id_carrera = Column(Integer, ForeignKey("carreras.id_carrera"))
    carrera = relationship("Carrera", back_populates="cursos")
    materias = relationship("Materia", back_populates="curso")

class Materia(Base):
    __tablename__ = "materias"
    id_materia = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(255), index=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"))
    curso = relationship("Curso", back_populates="materias")