from validation.project_validation import ProjectValidator
from data.proyect_data_base import  get_all_proyects, proyect_by_id, add_project_to_db, match_projects_with_keywords, add_keywords_in_database
from sqlalchemy.orm import Session

#@ Octener todas las carreras de la base de datos:
async def fetch_proyects(db: Session): 
    return get_all_proyects(db)


#@ Octener todas las carreras de la base de datos:
async def fetch_proyect_by_id(id_proyect: str, db: Session): 
    return proyect_by_id(db, id_proyect)

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

    # Dividir las nuevas palabras clave por comas y limpiar espacios
    new_keys = [clave.strip() for clave in new_keyword.split(',') if clave.strip()]

    # Agregar las nuevas palabras claves a la BD recuperando su id:
    new_keyword_added = []
    for keys in list(set(new_keys)):
        id_new_keyword = add_keywords_in_database(keys, db)
        new_keyword_added.append(id_new_keyword)

    # Combinar las palabras clave existentes con las nuevas
    ids_of_all_keywords = keywords + new_keyword_added

    # Agregar los datos del proyecto a la BD recuperando su id:
    id_project = add_project_to_db(project_data, db)

    for id_palabra in ids_of_all_keywords:
        match_projects_with_keywords(id_palabra, id_project, db)

