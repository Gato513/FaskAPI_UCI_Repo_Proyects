import shutil
from fastapi import UploadFile, HTTPException, status
from pathlib import Path
from config.server_config import store_dir, static_covers_dir
from uuid import uuid4

def handle_document_path(file_name, path):
    store_path = Path(path) / file_name
    return store_path


def write_file_to_path(uploaded_file: UploadFile, file_name: str, path: Path):
    store_path = handle_document_path(file_name, path)
    store_path.parent.mkdir(parents=True, exist_ok=True)
    
    with store_path.open("wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)


def save_uploaded_file(uploaded_file: UploadFile, file_name: str):
    try:
        write_file_to_path(uploaded_file, file_name, store_dir)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar el archivo: {str(e)}"
        )


def save_cover_image(cover_uploaded: UploadFile) -> str:
    try:
        if cover_uploaded.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se permiten imágenes PNG o JPEG."
            )
        
        imagen_filename = f"{uuid4().hex}_{cover_uploaded.filename}"

        write_file_to_path(cover_uploaded, imagen_filename, static_covers_dir)

        return imagen_filename
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar la portada: {str(e)}"
        )


