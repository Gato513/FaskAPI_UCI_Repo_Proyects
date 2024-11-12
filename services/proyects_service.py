import shutil
from validation.project_validation import ProjectValidator
from fastapi import HTTPException, status
from data.proyect_data_base import (
    get_all_proyects, 
    proyect_by_id, add_project_to_db,
    match_projects_with_keywords,
    add_keywords_in_database,
    get_all_subjects_by_course,
    get_all_students_by_course,
    associate_subjects,
    associate_documents,
    associate_students
)
from util.save_uploaded_file import save_uploaded_file, handle_document_path
from sqlalchemy.orm import Session

#@ Octener todas las carreras de la base de datos:
async def fetch_proyects(db: Session): 
    return get_all_proyects(db)


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

    there_are_words = ProjectValidator.validate_keywords(keywords, new_keyword)

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
async def handle_association_aggregation(associated_data: dict, db: Session) -> str:
    try:
        id_project = associated_data["id_project"]

        #( Asociar Materias
        if associated_data["subjects"]:
            for materia_id in associated_data["subjects"]:
                associate_subjects(materia_id, id_project, db)

        #( Asociar Alumnos
        if associated_data["students"]:
            for usuario_id in associated_data["students"]:
                associate_students(usuario_id, id_project, db)

        #( Asociar Documentos
        if  ProjectValidator.validate_documents(associated_data["documents"]):
            
            for document in associated_data["documents"]:
                file_name = document.filename
                save_uploaded_file(document, file_name)
                associate_documents(file_name, id_project, db)
            print("Archivos guardados correctamente.")
        else:
            print("No se recibieron archivos para asociar.")

        return {"message": "Asociaciones agregadas exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al asociar datos al proyecto: {str(e)}")
