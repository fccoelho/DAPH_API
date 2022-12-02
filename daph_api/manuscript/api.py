from typing import List
from ninja import Router, File, Form
from ninja.pagination import paginate, PageNumberPagination
from registry.models import Author, Manuscript
from ninja import Query, Schema, ModelSchema
from ninja.files import UploadedFile
from django.contrib.auth.models import User
from registry.models import Author, Manuscript
from ninja.security import django_auth
from ..file.upload import upload_file
from datetime import datetime
import web3

router = Router()

w3 = web3.Web3(web3.HTTPProvider("http://localhost:8545"))


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


submit_manuscript_contract_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "idmanuscript", "type": "string"}
        ],
        "name": "submit_manuscript",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


@router.post("/upload", auth=django_auth)
def create(request, title: str = Form(...), file: UploadedFile = File(...)):
    id, path = upload_file(file.read())

    author = Author.objects.get(user_id=request.auth)
    manuscript = Manuscript.objects.create(title=title, date_submission=datetime.now())
    manuscript.authors.add(author.id)

    dpublish_contract = w3.eth.contract(address="<DPUPLISH_CONTRACT_ADDRESS", abi=submit_manuscript_contract_abi)
    tx = dpublish_contract.functions.submit_manuscript(id).transact({"from": author.address})

    return {"file_path": path, "transaction": tx.hex()}
