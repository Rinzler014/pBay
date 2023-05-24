from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="home"),
    path("signup/", views.signup, name="signup"),
    path("landing/", views.landing, name="landing"),
    path("details/", views.details, name="details"),

]