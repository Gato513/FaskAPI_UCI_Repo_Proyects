from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from config.database_config import Base

#@ Relaciones Muchos a Muchos:

class ClavesDeProyectos(Base):
    __tablename__ = 'claves_de_proyectos'
    id_claves = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_palabra = Column(Integer, ForeignKey('palabras_clave.id_palabra_clave'), primary_key=True)
    id_proyecto = Column(Integer, ForeignKey('proyectos.id_proyecto'), primary_key=True)

    palabras_clave = relationship("PalabrasClave", back_populates="proyectos_asociados")
    proyecto = relationship("Proyecto", back_populates="palabras_claves")


class ProyectosPorMateria(Base):
    __tablename__ = 'proyectos_por_materias'
    id_proy_por_mater = Column(Integer, primary_key=True, autoincrement=True, index=True)
    materia_id = Column(Integer, ForeignKey('materias.id_materia'), primary_key=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id_proyecto'), primary_key=True)

    materia = relationship("Materia", back_populates="proyectos_asociados")
    proyecto = relationship("Proyecto", back_populates="materias_asociadas")


class ElementosPorProyecto(Base):
    __tablename__ = 'elementos_por_proyectos'
    id_elem_por_proy = Column(Integer, primary_key=True, autoincrement=True, index=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id_proyecto'), nullable=False)
    ruta_de_elemento = Column(String(255), nullable=False)

    proyecto = relationship("Proyecto", back_populates="elementos_asociados")


class ProfesoresFacultades(Base):
    __tablename__ = "profesores_facultades"
    id_prof_facultad = Column(Integer, primary_key=True, autoincrement=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    facultad_id = Column(Integer, ForeignKey("facultad.id_facultad"), primary_key=True)


class PermisoModificacionProyecto(Base):
    __tablename__ = 'permiso_modificacion_proyecto'
    id_permiso_modif = Column(Integer, primary_key=True, autoincrement=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id_proyecto"), primary_key=True)

    # Registrar la última modificación
    ultima_modificacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="proyectos_permitidos")
    proyecto = relationship("Proyecto", back_populates="usuarios_autorizados")


#@ Relaciones Uno a Muchas:
class PalabrasClave(Base):
    __tablename__ = "palabras_clave"
    id_palabra_clave = Column(Integer, primary_key=True, autoincrement=True, index=True)
    palabras_clave = Column(String(50), nullable=False, unique=True)

    proyectos_asociados = relationship("ClavesDeProyectos", back_populates="palabras_clave")


class Proyecto(Base):
    __tablename__ = "proyectos"
    id_proyecto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre_proyecto = Column(String(255), nullable=False)

    portada = Column(String(255), nullable=False)

    descripcion_proyecto = Column(Text, nullable=False)
    fecha_original_proyecto = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    #$ Relacion mucho a mucho con palabras claves:
    palabras_claves = relationship("ClavesDeProyectos", back_populates="proyecto")

    #$ Relacion mucho a mucho con materias:
    materias_asociadas = relationship("ProyectosPorMateria", back_populates="proyecto")

    #$ Usuarios (alumnos) autorizados para modificar el proyecto
    usuarios_autorizados = relationship("PermisoModificacionProyecto", back_populates="proyecto")

    #$ Relación uno a muchos con elementos
    elementos_asociados = relationship("ElementosPorProyecto", back_populates="proyecto")

    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"), nullable=False)
    id_carrera  = Column(Integer, ForeignKey("carreras.id_carrera"), nullable=False)
    id_curso    = Column(Integer, ForeignKey("cursos.id_curso"), nullable=False)

    facultad    = relationship("Facultad", back_populates="proyectos") 
    carrera     = relationship("Carrera", back_populates="proyectos")  
    curso       = relationship("Curso", back_populates="proyectos")    

    # Relación con auditorías
    auditorias = relationship("Auditoria", back_populates="proyecto")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String(50), nullable=False, unique=True)
    user_phone = Column(String(20), nullable=False, unique=True)
    user_document = Column(String(20), nullable=False, unique=True)
    user_address = Column(String(100), nullable=False)
    user_matricula = Column(String(100), nullable=True) # Solo nesesario si es un Alumno.
    user_email = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    role = Column(String(10), nullable=False, default="alumno") # Rol: "Admin", "profesor" y "alumno"
    
    #$ Seccion de Relaciones de los Usuarios:
    # Clave foránea a facultad si es alumno
    facultad_id = Column(Integer, ForeignKey("facultad.id_facultad"), nullable=True)

    # Relación con facultad para los alumnos
    facultad = relationship("Facultad", foreign_keys=[facultad_id], back_populates="alumnos")

    # Relación muchos-a-muchos para los profesores
    facultades = relationship("Facultad", secondary="profesores_facultades", back_populates="profesores")

    # Proyectos que el alumno tiene permiso de modificar
    proyectos_permitidos = relationship("PermisoModificacionProyecto", back_populates="usuario")

    # Relación con auditoría (un usuario puede tener varias auditorías)
    auditorias = relationship("Auditoria", back_populates="usuario")

class Facultad(Base):
    __tablename__ = "facultad"
    id_facultad = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_facultad = Column(String(255), nullable=False)
    is_activated = Column(Boolean, nullable=False, default=True)
    carreras = relationship("Carrera", back_populates="facultad")

    # Relación de uno-a-muchos hacia proyectos
    proyectos = relationship("Proyecto", back_populates="facultad")
    
    # Relación de uno-a-muchos para alumnos
    alumnos = relationship("Usuario", back_populates="facultad", primaryjoin="and_(Usuario.facultad_id == Facultad.id_facultad, Usuario.role == 'alumno')")

    # Relación muchos-a-muchos para profesores
    profesores = relationship("Usuario", secondary="profesores_facultades", back_populates="facultades")


class Carrera(Base):
    __tablename__ = "carreras"
    id_carrera = Column(Integer, primary_key=True, index=True)
    nombre_carrera = Column(String(255), index=True)
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"))
    facultad = relationship("Facultad", back_populates="carreras")
    cursos = relationship("Curso", back_populates="carrera")

    # Relación de uno-a-muchos hacia Proyecto
    proyectos = relationship("Proyecto", back_populates="carrera")


class Curso(Base):
    __tablename__ = "cursos"
    id_curso = Column(Integer, primary_key=True, index=True)
    nombre_curso = Column(String(255), index=True)
    id_carrera = Column(Integer, ForeignKey("carreras.id_carrera"))
    carrera = relationship("Carrera", back_populates="cursos")
    materias = relationship("Materia", back_populates="curso")

    # Relación de uno-a-muchos hacia Proyecto
    proyectos = relationship("Proyecto", back_populates="curso")


class Materia(Base):
    __tablename__ = "materias"
    id_materia = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(255), index=True)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"))
    curso = relationship("Curso", back_populates="materias")
    proyectos_asociados = relationship("ProyectosPorMateria", back_populates="materia")


#@ Sin Relaciones:
class Auditoria(Base):
    __tablename__ = "auditoria"
    id_auditoria = Column(Integer, primary_key=True, autoincrement=True)
    fecha_cambio = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    descripcion_cambio = Column(Text, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id_proyecto"), nullable=False)  

    # Relación con el modelo Usuario
    usuario = relationship("Usuario", back_populates="auditorias")

    # Relación con el modelo Proyecto
    proyecto = relationship("Proyecto", back_populates="auditorias")