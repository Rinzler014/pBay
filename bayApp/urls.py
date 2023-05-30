from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("signup/personal_info/", views.signup_2, name="signup_2"),
    path("signup/personal_info/account", views.signup_3, name="signup_3"),
    path("landing/<str:user>", views.landing, name="landing"),
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("details/", views.details, name="details"),
    path("mis_ventas/<str:user>", views.mis_ventas, name="mis_ventas"),
    path("details/", views.details, name="details"),
    path("bids/", views.bids, name="bids"),
    path("my_products/", views.my_products, name="my_products"),
    path("details/", views.details, name="details"),
    path("bids/", views.bids, name="bids"),
    path("bids_state/", views.bids_state, name="bids_state"),
    path("my_products/", views.my_products, name="my_products"),
    path("new_product/",views.new_product, name="new_product")
]
