from ninja import NinjaAPI, Schema, File, Form
from ninja.files import UploadedFile
from ninja import ModelSchema
from registry.models import Author, Manuscript


api = NinjaAPI(csrf=True)


@api.get("/hello")
def hello(request):
    return "Hello world"


class UserDetails(Schema):
    first_name: str
    last_name: str
    email: str


@api.post("/user")
def create_user(request, details: UserDetails = Form(...)):
    a = Author.objects.create(**details.dict())
    return {"author": a.id}


class ManuscriptDetails(Schema):
    title: str
    author_email: str


@api.post("/upload")
def upload(
    request, details: ManuscriptDetails = Form(...), file: UploadedFile = File(...)
):
    data = file.read()
    mdet = details.dict()
    a = Author.objects.get(email=mdet["author_email"])
    m = Manuscript.objects.create(title=mdet["title"])
    m.author.add(a.id)
    return {"name": file.name, "len": len(data)}


###### Schemas ######


class ManuscriptSchema(ModelSchema):
    class Config:
        model = Manuscript
        model_fields = "__all__"
