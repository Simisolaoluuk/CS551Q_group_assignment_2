from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("institutions/", views.institution_list, name="institution_list"),
    path("institutions/<int:pk>/", views.institution_detail, name="institution_detail"),
    path("compare/", views.compare_institutions, name="compare_institutions"),
    path("top/", views.top_institutions, name="top_institutions"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("favourites/", views.favourite_list, name="favourite_list"),
    path("institutions/<int:pk>/favourite/add/", views.add_favourite, name="add_favourite"),
    path("institutions/<int:pk>/favourite/remove/", views.remove_favourite, name="remove_favourite"),
]