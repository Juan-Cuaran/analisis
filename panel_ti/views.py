from django.shortcuts import render, redirect
from .models import PoliticaSesion, Auditoria
from autenticacion.models import User
from .forms import PoliticaSesionForm
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse


# Create your views here.
def get_usuario_token(request):
    token = request.GET.get('token')
    if not token:
        return None
    try:
        access = AccessToken(token)
        user_id = access['user_id']
        return User.objects.get(id=user_id)
    except (TokenError, User.DoesNotExist):
        return None

def get_politica():
    politica = PoliticaSesion.objects.first()
    if not politica:
        politica = PoliticaSesion.objects.create()
    return politica

def ver_politica(request):
    context = {}
    if request.method == 'GET':
        usuario = get_usuario_token(request)
        if not usuario or usuario.role != 'gestor_TI':
            return redirect('/api/auth/login/')
                
        politica = get_politica()
        form = PoliticaSesionForm(instance=politica)
        context['form'] = form
        context['politica'] = politica
        return render(request, 'panel_ti/ver_politica.html', context)
    
def actualizar_politica(request):
    context = {}
    if request.method == 'POST':
        usuario = get_usuario_token(request)
        if not usuario or usuario.role != 'gestor_TI':
            return redirect('/api/auth/login/')

        politica = get_politica()
        # Capturar ANTES de form.is_valid() porque _post_clean() modifica la instancia en memoria
        valores_anteriores = {
            'limite_sesiones': politica.limite_sesiones,
            'tiempo_inactividad': politica.tiempo_inactividad,
            'tiempo_expiracion': politica.tiempo_expiracion,
            'tiempo_preservacion': politica.tiempo_preservacion,
        }
        form = PoliticaSesionForm(request.POST, instance=politica)
        if form.is_valid():
            politica_actualizada = form.save(commit=False)
            politica_actualizada.modificado_por = usuario
            politica_actualizada.save()

            #registrar la auditoria
            for campo, valor_anterior in valores_anteriores.items():
                valor_nuevo = getattr(politica_actualizada, campo)
                if valor_anterior != valor_nuevo:
                    Auditoria.objects.create(
                        acciones_modificads=campo,
                        valor_anterior=str(valor_anterior),
                        valor_nuevo=str(valor_nuevo),
                        usuario=usuario
                    )
            context['success'] = 'Política de sesión actualizada exitosamente'
            context['usuario'] = usuario
            form = PoliticaSesionForm(instance=politica_actualizada)
            context['form'] = form
            return render(request, 'panel_ti/ver_politica.html', context)
        else:
            context['errors'] = form.errors
            context['form'] = form
            return render(request, 'panel_ti/ver_politica.html', context)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def ver_auditoria(request):
    context = {}
    if request.method == 'GET':
        usuario = get_usuario_token(request)
        if not usuario or usuario.role != 'gestor_TI':
            return redirect('/api/auth/login/')

        auditorias = Auditoria.objects.all().order_by('-timestamp')
        context['auditorias'] = auditorias
        return render(request, 'panel_ti/ver_auditoria.html', context)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)