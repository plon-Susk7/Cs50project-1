from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.getContent,name="title"),
    path("seach",views.search,name="search"),
    path("create",views.createNewPage,name="create"),
    path("wiki/<str:heading>/edit",views.edit, name="edit"),
    path("random",views.rand,name="random")
    
]
