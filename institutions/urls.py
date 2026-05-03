from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("institutions/", views.institution_list, name="institution_list"),
    path("institutions/<int:pk>/", views.institution_detail, name="institution_detail"),
    path("compare/", views.compare_institutions, name="compare_institutions"),
    path("top/", views.top_institutions, name="top_institutions"),
]