from fastapi import HTTPException, status
from fastapi import UploadFile
from typing import List

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

    @staticmethod
    def validate_keywords(keywords: list, new_keyword: str):
        if keywords or new_keyword: 
            return True
        return False
    
    @staticmethod
    def validate_documents(documents: List[UploadFile]) -> bool:
        # Retorna True si al menos un documento tiene nombre y tamaño > 0, de lo contrario False
        return any(document.filename and document.size > 0 for document in documents)