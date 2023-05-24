from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signup_2/", views.signup_2, name="signup_2"),
    path("landing/", views.landing, name="landing"),
    path("details/", views.details, name="details"),

]