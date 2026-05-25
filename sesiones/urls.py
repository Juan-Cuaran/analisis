from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_sesion, name='create_sesion'),
    path('list/', views.list_sesions, name='list_sesions'),
    path('liberar/<int:sesion_id>/', views.liberar_sesion, name='liberar_sesion'),
    path('update_actividad/', views.update_actividad, name='update_actividad'),
    path('verify_sesion/', views.verify_sesion, name='verify_sesion'),
]
