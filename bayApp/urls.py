from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("signup/personal_info/", views.signup_2, name="signup_2"),
    path("signup/personal_info/account", views.signup_3, name="signup_3"),
    path("landing/", views.landing, name="landing"),
    path("details/", views.details, name="details"),
    path("edit_info_prod/", views.edit_info_prod, name="edit_info_prod")

]