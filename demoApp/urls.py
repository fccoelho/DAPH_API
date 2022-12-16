from django.urls import path
from django.urls.conf import include
from demoApp import views
from .views import SignUpView

urlpatterns = [
    path("", views.index, name="demo-index"),
    path("upload/", views.upload, name="demo-upload"),
    path("accounts/", include("django.contrib.auth.urls")), # User login/logout
    # path("accounts/django-sign-up/", SignUpView.as_view(), name="signup"), # signup using django auth
    path("accounts/sign-up", views.create_user, name="demo-sign-up"), # user creation using a post request to daph api
]
