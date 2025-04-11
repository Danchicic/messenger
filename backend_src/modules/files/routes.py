import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from core.config import config

router = APIRouter()


@router.get('/uploads/{file_hex}')
async def get_file(file_hex: str):
    file_path = os.path.join(config.base_dir, "uploads", file_hex)

    # Проверка существования файла
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        media_type="application/octet-stream",  # Общий MIME-тип
        filename='_'.join(file_hex.split("_")[1:])  # Позволяет браузеру предложить скачивание
    )
