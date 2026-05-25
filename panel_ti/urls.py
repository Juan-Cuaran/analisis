from django.urls import path
from . import views

app_name = 'panel_ti'

from django.urls import path
from . import views

urlpatterns = [
    path('politicas/', views.ver_politica, name='ver_politica'),
    path('politicas/actualizar/', views.actualizar_politica, name='actualizar_politica'),
    path('auditoria/', views.ver_auditoria, name='ver_auditoria'),
]