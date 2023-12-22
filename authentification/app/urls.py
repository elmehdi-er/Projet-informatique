from django.urls import path
from app import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('upload/', views.upload_image, name='upload_image'),
    path('login', views.logIn, name='login'),
    path('home', views.home, name="home"),
    path('charger', views.charger, name='charger'),
    path('charts', views.charts, name="charts"),
    path('tables', views.tables, name="tables"),
    path('tables2', views.tables2, name="tables2"),
    path('tables3', views.tables3, name="tables3"),


]