from typing import List
from django.forms import ValidationError
from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from registry.models import Author, Manuscript
from ninja import Query, Schema, ModelSchema

router = Router()


class SearchQuery(Schema):
    query: str = ""
    order: str = "-date_submission"


class AuthorSchema(ModelSchema):
    class Config:
        model = Author
        model_fields = ["id", "user_id", "is_reviewer"]

class ManuscriptSchema(ModelSchema):
    authors: List[AuthorSchema] = []

    class Config:
        model = Manuscript
        model_fields = ["id", "title", "date_submission"]


@router.get("/search", response=List[ManuscriptSchema])
@paginate(PageNumberPagination, page_size=20)
def search(request, query: SearchQuery = Query(...)):
    return Manuscript.objects.filter(title__icontains=query.query).order_by(query.order)
