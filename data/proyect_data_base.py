# Capa de Acceso a Datos (Repositorio / Base de Datos)
from decorators.db_transaction_manager import DBTransactionManager
from models.all_model import(
    Proyecto,
    ClavesDeProyectos,
    ProyectosPorMateria,
    ElementosPorProyecto,
    PermisoModificacionProyecto,
    PalabrasClave,
    Materia,
    Usuario,
    Curso
)
from sqlalchemy.orm import Session
from typing import List, Optional

#@ Función para obtener todas las carreras:
@DBTransactionManager.handle_transaction
def get_all_proyects(db: Session) -> List[Proyecto]:
    return db.query(Proyecto).all()

#@ Función para obtener un proyecto por id:
@DBTransactionManager.handle_transaction
def proyect_by_id(db: Session, id_proyect: str) -> Optional[Proyecto]:
    return db.query(Proyecto).filter(Proyecto.id_proyecto == id_proyect).first()

#@ Función para obtener todas las palabras clave:
@DBTransactionManager.handle_transaction
def get_all_keywords(db: Session) -> PalabrasClave:
    return db.query(PalabrasClave).all()

#@ Función para obtener todas las materias del curso:
@DBTransactionManager.handle_transaction
def get_all_subjects_by_course(id_curso: int, db: Session) -> List[Materia]:
    return db.query(Materia).filter(Materia.id_curso == id_curso).all()

#@ Función para obtener todos los estudiantes del curso:
@DBTransactionManager.handle_transaction
def get_all_students_by_course(id_curso: int, db: Session) -> List[Usuario]:

    #$ Consulta para obtener todos los estudiantes (usuarios con rol 'alumno') del curso especificado
    return (
        db.query(Usuario)
        .join(Curso, Curso.id_carrera == Usuario.facultad_id)
        .filter(
            Usuario.role == "alumno",
            Curso.id_curso == id_curso
        )
        .all()
    )


#( Función para crear un proyecto en la base de datos
@DBTransactionManager.handle_transaction
def add_project_to_db(project_data: dict, db: Session) -> int:
    new_project = Proyecto(
        nombre_proyecto=project_data["nombre_proyecto"],
        descripcion_proyecto=project_data["descripcion_proyecto"],
        id_facultad=project_data["facultad_id"],
        id_carrera=project_data["carrera_id"],
        id_curso=project_data["curso_id"]
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project.id_proyecto


#$ Función para agregar nuevas palabras clave a la BD:
@DBTransactionManager.handle_transaction
def add_keywords_in_database(keyword: str, db: Session):

    # Verificar si la palabra clave ya existe
    existing_keyword = db.query(PalabrasClave).filter(PalabrasClave.palabras_clave == keyword).first()

    if existing_keyword:
        return existing_keyword.id_palabra_clave # Devolver el ID de la palabra existente

    new_keyword = PalabrasClave(palabras_clave=keyword)
    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)

    return new_keyword.id_palabra_clave


#% Función para relacionar proyectos con palabras clave:
@DBTransactionManager.handle_transaction
def match_projects_with_keywords(id_palabra: int, id_proyecto: int, db: Session):
    new_key_per_project = ClavesDeProyectos(
        id_palabra = id_palabra,
        id_proyecto = id_proyecto
    )

    db.add(new_key_per_project)
    db.commit()
    db.refresh(new_key_per_project)


#% Función para relacionar proyectos con palabras clave:
@DBTransactionManager.handle_transaction
def associate_subjects(materia_id: int, id_project: int, db: Session):
    association = ProyectosPorMateria(materia_id = materia_id, proyecto_id = id_project)
    db.add(association)
    db.commit()
    db.refresh(association)


#% Función para relacionar proyectos con palabras clave:
@DBTransactionManager.handle_transaction
def associate_documents(file_name: str, id_project: int, db: Session):
    elemento_proyecto = ElementosPorProyecto(
        proyecto_id= id_project,
        ruta_de_elemento=file_name
    )
    db.add(elemento_proyecto)
    db.commit()
    db.refresh(elemento_proyecto)


#% Función para relacionar proyectos con palabras clave:
@DBTransactionManager.handle_transaction
def associate_students(usuario_id: int, id_project: int, db: Session):
    permiso = PermisoModificacionProyecto(
        usuario_id=usuario_id,
        proyecto_id= id_project
    )
    db.add(permiso)
    db.commit()
    db.refresh(permiso)