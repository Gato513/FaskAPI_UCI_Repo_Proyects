from fastapi import HTTPException, status

class ProjectValidator:
    @staticmethod
    def validate_nombre_proyecto(nombre_proyecto: str):
        if not nombre_proyecto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agregue un nombre de proyecto")

    @staticmethod
    def validate_descripcion_proyecto(descripcion_proyecto: str):
        if not descripcion_proyecto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agregue una descripción del proyecto")

    @staticmethod
    def validate_id(id_value: int, id_name: int):
        if not id_value.isdigit() or int(id_value) <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El {id_name} debe ser un número positivo")