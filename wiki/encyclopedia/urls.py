from django.urls import path

from . import views
app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("add/",views.addentry,name = "addentry"),
    path("wiki/<str:title>",views.getentry ,name="getentry"),
    path("random",views.randomentry,name="random"),
    path("search",views.searchentry,name="search"),
    path("edit/",views.editentry,name="editentry")
    
]
