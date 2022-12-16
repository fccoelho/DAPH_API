from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
def index(request):
    return render(request, "demoApp/index.html")

def create_user(request):
    return render(request, "demoApp/create-user.html")

def upload(request):
    return render(request, "demoApp/upload.html")