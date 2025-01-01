from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from settings import AWS_PROFILE_FILES_FOLDER, AWS_BUCKET_NAME, AWS_FILE_URL, AWS_DOCUMENT_FILES_FOLDER
import uuid
from middleware.s3 import get_s3_client
from mimetypes import guess_type
from enum import Enum
router = APIRouter()

class AWSFolderMapper(str, Enum):
    profile = AWS_PROFILE_FILES_FOLDER
    event = AWS_DOCUMENT_FILES_FOLDER

@router.post("/{folder}/upload")
def upload_profile_file(folder:AWSFolderMapper,file: UploadFile = File(...)):
    try:
        folder_name = folder
        s3_client = get_s3_client()
        mime_type, _ = guess_type(file.filename)
        file.filename = str(uuid.uuid4())
        if not mime_type:
            mime_type = "application/octet-stream"
        target_path = folder_name + "/" + file.filename
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, target_path, ExtraArgs={"ContentType": mime_type})
        return JSONResponse(content={"file_name": file.filename,"mime_type": mime_type, "file_url": AWS_FILE_URL+ target_path, "message": "File uploaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error uploading file: " + str(e)}, status_code=500)
    
@router.get("/download/{folder}/{filename}")
def download_file(folder: AWSFolderMapper,filename: str):
    try:
        s3_client = get_s3_client()
        file_path = folder + "/" + filename
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=file_path)
        file_stream = response['Body']
        return StreamingResponse(
            file_stream,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return {"error": str(e)}, 500
    
@router.post("/{folder}/upload/{filename}")
def upload_profile_file(filename:str,folder:AWSFolderMapper,file: UploadFile = File(...)):
    try:
        folder_name = folder
        s3_client = get_s3_client()
        mime_type, _ = guess_type(file.filename)
        file.filename = filename
        if not mime_type:
            mime_type = "application/octet-stream"
        target_path = folder_name + "/" + file.filename
        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, target_path, ExtraArgs={"ContentType": mime_type})
        return JSONResponse(content={"file_name": file.filename,"mime_type": mime_type, "file_url": AWS_FILE_URL+ target_path, "message": "File uploaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error uploading file: " + str(e)}, status_code=500)