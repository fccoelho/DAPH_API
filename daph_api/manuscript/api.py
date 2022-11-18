from typing import List
from django.forms import ValidationError
from ninja import Router, File
from ninja.pagination import paginate, PageNumberPagination
from registry.models import Author, Manuscript
from ninja import Query, Schema, ModelSchema
from ninja.files import UploadedFile
from ..file.upload import upload_file
router = Router()


class SearchQuery(Schema):
    query: str = ""
    order: str = "-date_submission"


class AuthorSchema(ModelSchema):
    class Config:
        model = Author
        model_fields = ["id"]

class ManuscriptSchema(ModelSchema):
    authors: List[AuthorSchema] = []

    class Config:
        model = Manuscript
        model_fields = ["id", "title", "date_submission"]


@router.get("/search", response=List[ManuscriptSchema])
@paginate(PageNumberPagination, page_size=20)
def search(request, query: SearchQuery = Query(...)):
    return Manuscript.objects.filter(title__icontains=query.query).order_by(query.order)

@router.post("/upload")
def create(request, file: UploadedFile = File(...)):
    path = upload_file(file.read())
    return {"file_path": path}
