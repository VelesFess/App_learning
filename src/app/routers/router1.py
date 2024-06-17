from fastapi import APIRouter, File, UploadFile

router = APIRouter()
Response = ""


@router.get("/", response_model=Response)
def process(file: UploadFile = File(...)):
    # Do work
    return
