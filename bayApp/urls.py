from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="home"),
    path("signup/", views.signup),
    path("landing/", views.landing),

]