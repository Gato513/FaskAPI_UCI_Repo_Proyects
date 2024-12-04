from fileinput import filename
import shutil
from data.audits_data_base import register_audit_entry
from models.all_model import ElementosPorProyecto, Proyecto, Usuario
from validation.project_validation import ProjectValidator
from fastapi import HTTPException, status
from typing import Optional
from data.proyect_data_base import (
    proyect_by_id, 
    add_project_to_db,
    match_projects_with_keywords,
    add_keywords_in_database,
    get_all_subjects_by_course,
    get_all_students_by_course,
    associate_subjects,
    associate_documents,
    associate_students,
    delete_project_by_id,
    delete_relation_by_id,
    update_project_in_db,
    get_filtered_projects
)

from util.save_uploaded_file import save_uploaded_file, save_cover_image
from sqlalchemy.orm import Session


#@ Obtener proyectos filtrados de la base de datos
async def fetch_proyects(
    db: Session,
    nombre_proyecto: Optional[str] = None,
    facultad: Optional[str] = None,
    carrera: Optional[str] = None,
    curso: Optional[str] = None,
):
    # Crear un diccionario de filtros basado en los parámetros recibidos
    filters = {
        "nombre_proyecto": nombre_proyecto,
        "facultad": facultad,
        "carrera": carrera,
        "curso": curso,
    }

    # Filtrar valores vacíos o nulos
    filters = {key: value for key, value in filters.items() if value}

    # Llamar a la función de la capa de datos
    return get_filtered_projects(db, filters)

#@ Octener todas las carreras de la base de datos:
async def fetch_proyect_by_id(id_proyect: str, db: Session): 
    # Recupera el proyecto por su ID
    project = proyect_by_id(db, id_proyect)

    # Procesa cada elemento asociado para actualizar su ruta y nombre
    for elemento in project.elementos_asociados:
        file_name = elemento.ruta_de_elemento   # Obtén el nombre del archivo
        elemento.name = file_name.capitalize()  # Asigna el nombre de archivo al atributo 'name'
        elemento.download_url = f"/store/{file_name}"

    return project

#@ Octener todas las materias de la base de datos:
async def fetch_all_subjects(id_curso: int, db: Session): 
    return get_all_subjects_by_course(id_curso, db)

#@ Octener todos los estudiantes de la base de datos:
async def fetch_all_students(id_curso: int, db: Session): 
    return get_all_students_by_course(id_curso, db)


#$ Crear Nuevo Proyecto:
async def create_new_project(project_data: dict, db: Session) -> str:
    
    # Llamar a las validaciones de la clase ProjectValidator 
    ProjectValidator.validate_nombre_proyecto(project_data['nombre_proyecto'])
    ProjectValidator.validate_descripcion_proyecto(project_data['descripcion_proyecto'])
    ProjectValidator.validate_id(project_data['facultad_id'], "ID de la facultad")
    ProjectValidator.validate_id(project_data['carrera_id'], "ID de la carrera")
    ProjectValidator.validate_id(project_data['curso_id'], "ID del curso")

    keywords = project_data.pop("palabras_clave")
    new_keyword = project_data.pop("nueva_palabra_clave")
    document = project_data.pop("document")

    there_are_words = ProjectValidator.validate_keywords(keywords, new_keyword)

    #% Escribir la imagen de portada en el servidor:
    project_data["imagen_filename"] = save_cover_image(document)

    # Agregar los datos del proyecto a la BD recuperando su id:
    id_project = add_project_to_db(project_data, db)


    if there_are_words:
        # Dividir las nuevas palabras clave por comas y limpiar espacios
        new_keys = [clave.strip() for clave in new_keyword.split(',') if clave.strip()]

        # Agregar las nuevas palabras claves a la BD recuperando su id:
        new_keyword_added = []
        for keys in list(set(new_keys)):
            id_new_keyword = add_keywords_in_database(keys, db)
            new_keyword_added.append(id_new_keyword)

        # Combinar las palabras clave existentes con las nuevas
        ids_of_all_keywords = keywords + new_keyword_added

        for id_palabra in ids_of_all_keywords:
            match_projects_with_keywords(id_palabra, id_project, db)


#$ Crear Asociaciones del Proyecto:
async def handle_association_aggregation(associated_data: dict, db: Session, user: Usuario) -> str:
    try:
        id_project = associated_data["id_project"]

        # Asociar documentos
        if ProjectValidator.validate_documents(associated_data["documents"]):
            for document in associated_data["documents"]:
                file_name = document.filename
                save_uploaded_file(document, file_name)
                associate_documents(file_name, id_project, db)

                # Registrar auditoría si el usuario es alumno
                if user.role == "alumno":
                    project = proyect_by_id(db, id_project)
                    descripcion = f"Documento '{file_name}' asociado al proyecto '{project.nombre_proyecto}'."
                    register_audit_entry(db, descripcion, user.id, id_project)

            print("Archivos guardados correctamente.")
        else:
            print("No se recibieron archivos para asociar.")

        return {"message": "Asociaciones agregadas exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asociar datos al proyecto: {str(e)}"
        )


#% Actualizar un Proyecto:
async def update_project(project_data: dict, db: Session, user: Usuario):
    try:
        # Obtener el proyecto existente
        existing_project = proyect_by_id(db, project_data["id"])
        if not existing_project:
            raise HTTPException(status_code=404, detail="El proyecto no existe")

        # Validar los campos principales del proyecto
        ProjectValidator.validate_nombre_proyecto(project_data["nombre_proyecto"])
        ProjectValidator.validate_descripcion_proyecto(project_data["descripcion_proyecto"])
        ProjectValidator.validate_id(project_data["facultad_id"], "ID de la facultad")
        ProjectValidator.validate_id(project_data["carrera_id"], "ID de la carrera")
        ProjectValidator.validate_id(project_data["curso_id"], "ID del curso")

        # Verificar si hubo cambios en alguno de los campos editables
        cambios = []
        if existing_project.nombre_proyecto != project_data["nombre_proyecto"]:
            cambios.append("nombre_proyecto")
        if existing_project.descripcion_proyecto != project_data["descripcion_proyecto"]:
            cambios.append("descripcion_proyecto")
        if existing_project.id_facultad != project_data["facultad_id"]:
            cambios.append("id_facultad")
        if existing_project.id_carrera != project_data["carrera_id"]:
            cambios.append("id_carrera")
        if existing_project.id_curso != project_data["curso_id"]:
            cambios.append("id_curso")

        # Si hubo cambios, actualizar el proyecto y registrar auditoría
        if cambios:
            updated_project = update_project_in_db(db, project_data["id"], project_data)

            # Registrar auditoría solo si el usuario es alumno
            if user.role == "alumno":
                descripcion = f"El proyecto: '{existing_project.nombre_proyecto}' ha sido modificado."
                register_audit_entry(db, descripcion, user.id, existing_project.id_proyecto)

            return {"message": "Proyecto actualizado con éxito", "project": updated_project}

        # Si no hubo cambios
        return {"message": "No se realizaron cambios en el proyecto."}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el proyecto: {str(e)}",
        )


#! Eliminar un proyecto y sus Relaciones:
async def delete_project_service(id_proyecto: int, db: Session):
    delete_project_by_id(id_proyecto, db)
    return {"message": f"Proyecto con ID {id_proyecto} eliminado exitosamente"}

#! Eliminar relacion con el proyecto: 
async def delete_relation_service(id_relation: int, type_of_relation: str, db: Session, user: Usuario):


    # Solo registrar auditoría si el tipo de relación es "element" (documento) y el usuario es un alumno
    if type_of_relation == "element" and user.role == "alumno":
        # Obtener el documento
        document = db.query(ElementosPorProyecto).filter(ElementosPorProyecto.id_elem_por_proy == id_relation).first()
        if document:
            # Obtener el proyecto al que pertenece el documento
            project = db.query(Proyecto).filter(Proyecto.id_proyecto == document.proyecto_id).first()
            if project:
                descripcion = f"Documento '{document.ruta_de_elemento}' eliminado del proyecto '{project.nombre_proyecto}'."
                register_audit_entry(db, descripcion, user.id, project.id_proyecto)

    # Llamar a la función de base de datos para eliminar la relación
    delete_relation_by_id(id_relation, type_of_relation, db)











