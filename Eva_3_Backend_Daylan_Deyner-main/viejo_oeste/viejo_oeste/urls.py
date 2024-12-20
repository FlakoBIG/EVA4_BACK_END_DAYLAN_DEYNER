"""viejo_oeste URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from personajes import views
from personajes.viewset import CaballoViewSet,VaqueroViewSet,ArmaViewSet
router = DefaultRouter()
router.register(r'caballos' , CaballoViewSet)
router.register(r'arma' , ArmaViewSet)
router.register(r'vaquero' , VaqueroViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('agregar/', views.agregar_vaquero),
    path('lista/', views.lista_vaquero),
    path('eliminar/<int:id>', views.eliminar_vaquero),
    path('actualizar/<int:id>', views.actualizar_vaquero),
    path('prueba/>', views.prueba),


    path('caballosos/',views.lista_caballos),
    path('agregar_caballo/',views.agregar_caballo),
    path('eliminar_caballo/<int:id>',views.eliminar_caballo),
    path('actualizar_caballo/<int:id>',views.actualizar_caballo),

    path('arma/', views.lista_armas),
    path('agregar_arma/', views.agregar_arma),
    path('eliminar_arma/<int:id>', views.eliminar_arma),
    path('actualizar_arma/<int:id>', views.actualizar_arma),

    path('agregar_caballo_vaquero/<int:id>/<int:id_vaquero>', views.agregar_caballo_vaquero),
    path('agregar_arma_vaquero/<int:id>/<int:id_vaquero>', views.agregar_arma_vaquero),
    path('desligar_Caballo/<int:id>', views.desligar_Caballo),
    path('desligar_Arma/<int:id>', views.desligar_Arma),

    path('api/', include(router.urls)), 
]
