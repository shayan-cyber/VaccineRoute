from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('select_location', views.select_location, name="select_location"),
    path('get_route/<str:center_id>/<str:pincode>/<str:lat>/<str:longi>/<str:cur_lat>/<str:cur_longi>', views.get_route, name="get_route"),
    path('about', views.about, name="about"),
    

]