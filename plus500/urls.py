from django.urls import  path
from plus500 import views

urlpatterns = [
    path('', views.get_data, name = "get_data"),
    path('', views.get_home_form, name = "get_home_form")
    #path('refpages/',views.refpages_detail, name = "refpages_detail")
]
