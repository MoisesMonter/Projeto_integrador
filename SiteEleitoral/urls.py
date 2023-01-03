from django.urls import path
from . import views

urlpatterns = [
    path('',views.Register,name='register'),
    path('home/',views.Home, name='home'),
    path('about_us/',views.About_us,name='about_us'),
    path('lista_eleicoes/',views.ListaEleicoes,name='lista_eleicoes'),
    path('login/',views.Login,name='login'),
    path('register/',views.Register,name='register'),
    path('suport_site/',views.Suport,name='Suport'),
    path('configuração/',views.Config,name='Config'),
]