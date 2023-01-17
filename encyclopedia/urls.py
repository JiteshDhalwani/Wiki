from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"), 
    path("wiki/<str:title>", views.entry, name = "entry"), 
    path("search", views.search, name = "search"),
    path("new_entry", views.newEntry, name = "new_entry"),
    path("edit/<str:title>", views.editEntry, name = "edit_entry"),
    path("save_entry", views.saveEntry, name = "save_entry"),
    path("random_page", views.randomPage, name = "random_page")

]
