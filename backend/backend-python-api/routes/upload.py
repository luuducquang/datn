from fastapi import APIRouter, File, UploadFile, HTTPException
import os
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOAD_DIRECTORY = "static/uploads/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return JSONResponse(content={"message": "File uploaded successfully", "file_path": file_location})
