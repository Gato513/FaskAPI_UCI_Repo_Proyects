import shutil
from fastapi import UploadFile, HTTPException, status
from pathlib import Path
from config.server_config import store_dir  # Asegúrate de que esta ruta es correcta

def handle_document_path(file_name):
    store_path = Path(store_dir) / file_name
    return store_path

# Esta función podría estar en tu servicio de proyecto
def save_uploaded_file(uploaded_file: UploadFile, file_name: str):
    try:
        
        store_path = handle_document_path(file_name)
        store_path.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe
        
        # Abre el archivo de destino en modo binario y copia el contenido del archivo cargado al archivo de destino
        with store_path.open("wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)  # 

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar el archivo: {str(e)}"
        )

