from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("signup/personal_info/", views.signup_2, name="signup_2"),
    path("signup/personal_info/account", views.signup_3, name="signup_3"),
    path("landing/<str:user_id>", views.landing, name="landing"),
    path("shopping_cart/<str:user_id>", views.shopping_cart, name="shopping_cart"),
    path("details/", views.details, name="details"),
    path("my_products/", views.my_products, name="my_products"),
    path("bids/<str:user_id>", views.auctions, name="bids"),
    path("bids_state/<str:user_id>", views.bids_state, name="bids_state"),
    path("new_product/<str:user_id>",views.new_product, name="new_product"),
    path("edit_info_prod/<str:user_id>", views.edit_info_prod, name="edit_info_prod"),
    path("mis_ventas/<str:user>", views.mis_ventas, name="mis_ventas"),
]