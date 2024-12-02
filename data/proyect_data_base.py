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
from enum import Enum
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

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


#& Funcion para octener todos los proyectos filtrados:
@DBTransactionManager.handle_transaction
def get_filtered_projects(db: Session, filters: dict) -> List[Proyecto]:
    query = db.query(Proyecto)

    if "nombre_proyecto" in filters and filters["nombre_proyecto"]:
        query = query.filter(Proyecto.nombre_proyecto.ilike(f"%{filters['nombre_proyecto']}%"))
    if "facultad" in filters and filters["facultad"]:
        query = query.filter(Proyecto.id_facultad == filters["facultad"])
    if "carrera" in filters and filters["carrera"]:
        query = query.filter(Proyecto.id_carrera == filters["carrera"])
    if "curso" in filters and filters["curso"]:
        query = query.filter(Proyecto.id_curso == filters["curso"])

    return query.all()


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

#( Función para agregar nuevas palabras clave a la BD:
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
    # Verificar si la relación ya existe
    exists = (
        db.query(ClavesDeProyectos)
        .filter(
            ClavesDeProyectos.id_palabra == id_palabra,
            ClavesDeProyectos.id_proyecto == id_proyecto
        )
        .first()
    )
    if exists:
        return 

    # Crear la relación si no existe
    new_key_per_project = ClavesDeProyectos(
        id_palabra=id_palabra,
        id_proyecto=id_proyecto
    )
    db.add(new_key_per_project)
    db.commit()
    db.refresh(new_key_per_project)

#% Función para relacionar proyectos con palabras clave:
@DBTransactionManager.handle_transaction
def associate_subjects(materia_id: int, id_project: int, db: Session):
    # Verificar si la relación ya existe
    exists = (
        db.query(ProyectosPorMateria)
        .filter(
            ProyectosPorMateria.materia_id == materia_id,
            ProyectosPorMateria.proyecto_id == id_project
        )
        .first()
    )
    if exists:
        return  # Si ya existe, no hacer nada

    # Crear la relación si no existe
    association = ProyectosPorMateria(materia_id=materia_id, proyecto_id=id_project)
    db.add(association)
    db.commit()
    db.refresh(association)

#% Función para relacionar proyectos con palabras clave:
@DBTransactionManager.handle_transaction
def associate_documents(file_name: str, id_project: int, db: Session):
    # Verificar si el archivo ya está asociado al proyecto
    exists = (
        db.query(ElementosPorProyecto)
        .filter(
            ElementosPorProyecto.proyecto_id == id_project,
            ElementosPorProyecto.ruta_de_elemento == file_name
        )
        .first()
    )
    if exists:
        return  # Si ya existe, no hacer nada

    # Crear la relación si no existe
    elemento_proyecto = ElementosPorProyecto(
        proyecto_id=id_project,
        ruta_de_elemento=file_name
    )
    db.add(elemento_proyecto)
    db.commit()
    db.refresh(elemento_proyecto)

#% Función para relacionar proyectos con palabras clave:
@DBTransactionManager.handle_transaction
def associate_students(usuario_id: int, id_project: int, db: Session):
    # Verificar si la relación ya existe
    exists = (
        db.query(PermisoModificacionProyecto)
        .filter(
            PermisoModificacionProyecto.usuario_id == usuario_id,
            PermisoModificacionProyecto.proyecto_id == id_project
        )
        .first()
    )
    if exists:
        return  # Si ya existe, no hacer nada

    # Crear la relación si no existe
    permiso = PermisoModificacionProyecto(usuario_id=usuario_id, proyecto_id=id_project)
    db.add(permiso)
    db.commit()
    db.refresh(permiso)


#! Eliminar Proyectos y su relaciones:
@DBTransactionManager.handle_transaction
def delete_project_by_id(id_proyecto: int, db: Session):

    # Elimina elementos relacionados
    db.query(ClavesDeProyectos).filter(ClavesDeProyectos.id_proyecto == id_proyecto).delete()
    db.query(ProyectosPorMateria).filter(ProyectosPorMateria.proyecto_id == id_proyecto).delete()
    db.query(ElementosPorProyecto).filter(ElementosPorProyecto.proyecto_id == id_proyecto).delete()
    db.query(PermisoModificacionProyecto).filter(PermisoModificacionProyecto.proyecto_id == id_proyecto).delete()

    # Elimina el proyecto
    proyecto = db.query(Proyecto).filter(Proyecto.id_proyecto == id_proyecto).first()
    db.delete(proyecto)
    db.commit()

#! Eliminar relaciones:
class RelationType(str, Enum):
    KEYWORD = "keyWord"
    SUBJECT = "materia"
    ELEMENT = "element"
    PERMISSION = "permisoModify"

@DBTransactionManager.handle_transaction
def delete_relation_by_id(id_relation: int, type_of_relation: RelationType, db: Session):
    relation_map = {
        RelationType.KEYWORD: (ClavesDeProyectos, ClavesDeProyectos.id_claves),
        RelationType.SUBJECT: (ProyectosPorMateria, ProyectosPorMateria.id_proy_por_mater),
        RelationType.ELEMENT: (ElementosPorProyecto, ElementosPorProyecto.id_elem_por_proy),
        RelationType.PERMISSION: (PermisoModificacionProyecto, PermisoModificacionProyecto.id_permiso_modif),
    }
    model_info = relation_map.get(type_of_relation)
    if not model_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de relación no válido."
        )

    model, id_attr = model_info
    db.query(model).filter(id_attr == id_relation).delete()
    db.commit()


#$ Actualizar el proyecto con los nuevos datos
@DBTransactionManager.handle_transaction
def update_project_in_db(db: Session, project_id: int, project_data: dict):
    try:
        project = db.query(Proyecto).filter(Proyecto.id_proyecto == project_id).first()
        if not project:
            raise HTTPException(
                status_code=404, detail="Proyecto no encontrado"
            )

        # Actualizar campos básicos del proyecto
        updatable_fields = [
            "nombre_proyecto", "descripcion_proyecto", 
            "id_facultad", "id_carrera", "id_curso"
        ]
        for field in updatable_fields:
            if field in project_data:
                setattr(project, field, project_data[field])

        db.commit()
        db.refresh(project)
        return project

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el proyecto: {str(e)}",
        )