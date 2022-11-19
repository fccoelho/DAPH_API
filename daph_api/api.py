from ninja import NinjaAPI, Schema, File, Form
from ninja.files import UploadedFile
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
from registry.models import Author, Manuscript, WalletAddress
from typing import List
from web3 import Web3, EthereumTesterProvider
from .manuscript.api import router as manuscript_router
from django.http import HttpResponse

if settings.DEBUG:
    w3 = Web3(EthereumTesterProvider())
else:
    w3 = Web3(Web3.HTTPProvider(
        'https://goerli.infura.io/v3/8f62d68e09944a559e788e8f73a7f4ed'))

api = NinjaAPI(csrf=True)
api.add_router('/manuscript', manuscript_router)

@api.get("/hello")
def hello(request):
    return "Hello world"


class UserDetails(Schema):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str


@api.post("/user")
def create_user(request, details: UserDetails = Form(...)):
    udict = details.dict()
    user = User.objects.create_user(**udict)
    author = Author.objects.create(user_id=user, is_reviewer=False)
    wallet_address = '0x26Ebb006D2FAe4eEF7e432b47f44ae93Bb223CA7'
    WalletAddress.objects.create(author_id=author, wallet_address=wallet_address)
    return {"author": author.id}


class ManuscriptDetails(Schema):
    title: str
    authors: List[str]

@api.post("/upload")
def upload(
    request, details: ManuscriptDetails = Form(...), file: UploadedFile = File(...)
):
    data = file.read()
    mdet = details.dict()
    authors = mdet['authors'][0].split(',')
    title = mdet['title']
    author_ids = []
    for author in authors:
        author_ids.append(get_object_or_404(Author, user_id__username=author).id)
    
    author_ids = list(dict.fromkeys(author_ids))
    manuscript = Manuscript.objects.create(title=title, file=file)
    manuscript.authors.set(author_ids)
    return {"manuscript": manuscript.id, "authors": author_ids}

@api.patch("/buy/{author_id}/{amount}")
def add_balance(request, author_id: int, amount: int):
    author = get_object_or_404(Author, id=author_id)
    author.balance += amount
    author.save()

    return {"balance": author.balance}

@api.patch("/pay/{author_id}/{amount}")
def pay_balance(request, author_id: int, amount: int):
    author = get_object_or_404(Author, id=author_id)
    if author.balance < amount:
        return HttpResponse(status=400, content="Insufficient balance")
    author.balance -= amount
    author.save()

    return {"balance": author.balance}

@api.get("/balance/{author_id}")
def get_balance(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return {"balance": author.balance}