from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("signup/personal_info/", views.signup_2, name="signup_2"),
    path("signup/personal_info/account", views.signup_3, name="signup_3"),
    path("landing/<str:user_id>", views.landing, name="landing"),
    path("shopping_cart/<str:user_id>", views.shopping_cart, name="shopping_cart"),
    path("details/<str:user_id>/<str:product_id>", views.details, name="details"),
    path("my_products/<str:user_id>", views.my_products, name="my_products"),
    path("bids/<str:user_id>", views.auctions, name="bids"),
    path("bids_state/<str:user_id>", views.bids_state, name="bids_state"),
    path("new_product/<str:user_id>",views.new_product, name="new_product"),
    path("edit_info_prod/<str:user_id>/<str:product_id>", views.edit_info_prod, name="edit_info_prod"),
    path("sales/<str:user>", views.sales, name="sales"),
    #path("shopping_cart/<str:user_id>", views.addProductShoppingCart, name="addProductShoppingCart")
    path("addProductShoppingCart/", views.addProductShoppingCart, name="addProductShoppingCart"),
    path("eraseProductShoppingCart/", views.eraseProductShoppingCart, name="eraseProductShoppingCart"),
    path("my_profile/<str:user_id>", views.myProfile, name="my_profile"),
    path('search/<str:user_id>', views.search_products, name='search_products'),
    #path("updatePersonalInfo/", views.updatePersonalInfo, name="updatePersonalInfo")
    path('get-product-suggestions/', views.get_product_suggestions, name='get_product_suggestions'),
]