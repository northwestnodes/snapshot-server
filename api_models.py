from pydantic import BaseModel

class ResponseModel(BaseModel):
    status: str = 'success'
    message: str

class ProcessFileModel(BaseModel):
    filename: str
    network: str

class DefaultResponses():
    success = ResponseModel(status='success',message='')
    error = ResponseModel(status='error',message='An unhandled error occurred')