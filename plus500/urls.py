from django.urls import  path
from plus500 import views

urlpatterns = [
    path('', views.data_updated, name = "data_updated"),
    path('', views.get_home_form, name = "get_home_form")
    #path('refpages/',views.refpages_detail, name = "refpages_detail")
]
