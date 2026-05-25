from datetime import timedelta

from django.utils import timezone

from django.shortcuts import render
from .models import SesionActiva, RegistroActividad
from panel_ti.models import PoliticaSesion
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from autenticacion.models import User

# Create your views here.

#Crear la sesion con el token generado en el login
def create_sesion(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    token = request.POST.get('token')
    if not token:
        return JsonResponse({'error': 'Token es requerido para crear sesión'}, status=400)

    #Decodificar el token para obtener el usuario
    access = AccessToken(token)
    user_id = access['user_id']
    user = User.objects.get(id=user_id)

    # Verificar limite de sesiones activas usando la política definida en panel_ti
    policy = PoliticaSesion.objects.first()
    LIMITE = policy.limite_sesiones if policy else 3
    sesiones_activas = SesionActiva.objects.filter(user=user, estado='activa').count()
    if sesiones_activas >= LIMITE:
        return JsonResponse({'error': 'Límite de sesiones activas alcanzado'}, status=400)
    
    sesion = SesionActiva.objects.create(
        user=user,
        dispositivo=request.META.get('HTTP_USER_AGENT', 'Desconocido'),
        token=token,
        estado='activa'
    )
    sesion.save()
    return JsonResponse({'message': 'Sesión creada exitosamente'})

#listar las sesiones
def list_sesions(request):
    context = {}
    if request.method == "GET":
        token = request.GET.get('token')
        if not token:
            context['error'] = 'Token es requerido para listar sesiones'
        #decodificar el token para obtener el usuario
        
        access = AccessToken(token)
        user_id = access['user_id']
        user = User.objects.get(id=user_id)

        # obtener las sesiones del usuario sean activas o inactivas
        sesiones = SesionActiva.objects.filter(user=user)
        context['sesiones'] = sesiones
    else:
        context['error'] = "Método no permitido"
    return render(request, 'sesiones/list_sesions.html', context)

def liberar_sesion(request, sesion_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        sesion = SesionActiva.objects.get(id=sesion_id, user=request.user)
        sesion.estado = 'inactiva'
        sesion.save()
        return JsonResponse({'message': 'Sesión liberada exitosamente'})
    except SesionActiva.DoesNotExist:
        return JsonResponse({'error': 'Sesión no encontrada o no pertenece al usuario'}, status=404)

#Actualiza la ultima actividad registrada y en progreso
def update_actividad(request):
    if request.method == "POST":
        token = request.POST.get('token')
        actividad = request.POST.get("actividad_progreso")
        if not token:
            return JsonResponse ({'error': 'No se ha encontrado el token'}, status=400)
        if not actividad:
            return JsonResponse ({'error': 'No se ha encontrado la actividad'}, status=400)
        try:
            sesion = SesionActiva.objects.get(token=token, user=request.user)
            sesion.ultima_actividad = timezone.now()
            sesion.actividad_progreso = actividad
            sesion.save()
            RegistroActividad.objects.create(sesion=sesion, actividad=actividad)
            return JsonResponse({'message': 'Actividad actualizada exitosamente'})
        except SesionActiva.DoesNotExist:
            return JsonResponse({'error': 'Sesión no encontrada o no pertenece al usuario'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#Verificar todas las sesiones y desactivar las que no esten activas
def verify_sesion(request):
    if request.method == "POST":
        TIEMPO_INACTIVIDAD = 5 # minutos
        TIEMPO_ACTUAL = timezone.now()
    
        sesiones = SesionActiva.objects.filter(user=request.user, token__isnull=False)
        desactivadas = 0
        for sesion in sesiones:
            tiempo_inactividad = TIEMPO_ACTUAL - sesion.ultima_actividad
            if not sesion.actividad_progreso and tiempo_inactividad.total_seconds() > timedelta(minutes=TIEMPO_INACTIVIDAD):
                sesion.estado = "inactiva"
                sesion.save()
                desactivadas += 1
        return JsonResponse({'message': f'Sesiones verificadas exitosamente. {desactivadas} sesiones desactivadas.'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    