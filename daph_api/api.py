from ninja import NinjaAPI, Schema, File, Form
from ninja.files import UploadedFile
from django.contrib.auth.models import User
from django.conf import settings
from registry.models import Author, Manuscript, WalletAddress
from web3 import Web3, EthereumTesterProvider

if settings.DEBUG:
    w3 = Web3(EthereumTesterProvider())
else:
    w3 = Web3(Web3.HTTPProvider(
        'https://goerli.infura.io/v3/8f62d68e09944a559e788e8f73a7f4ed'))

api = NinjaAPI(csrf=True)


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
    wallet_address = '0x26Ebb006D2FAe4eEF7e432b47f44ae93Bb223CA7'
    WalletAddress.objects.create(user_id=user, wallet_address=wallet_address)
    author = Author.objects.create(user_id=user)
    return {"author": author.id}


class ManuscriptDetails(Schema):
    title: str
    author_email: str


@api.post("/upload")
def upload(
    request, details: ManuscriptDetails = Form(...), file: UploadedFile = File(...)
):
    data = file.read()
    mdet = details.dict()
    user = User.objects.get(email=mdet["author_email"])
    author = Author.objects.get(user_id=user)
    manuscript = Manuscript.objects.create(title=mdet["title"])
    manuscript.authors.add(author.id)
    return {"name": file.name, "len": len(data)}
