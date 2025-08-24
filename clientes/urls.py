from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para API REST
router = DefaultRouter()
router.register('clientes', views.ClienteViewSet)

app_name = 'clientes'

urlpatterns = [
    # URLs de la API REST
    path('api/', include(router.urls)),
    
    # URLs de las vistas web tradicionales
    path('clientes/', views.lista_clientes, name='lista'),
    path('clientes/<int:pk>/', views.detalle_cliente, name='detalle'),
    path('clientes/crear/', views.crear_cliente, name='crear'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar'),
]
