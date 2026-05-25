from django.shortcuts import render, redirect
from .models import User
from .form import UserRegistrationForm
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
def register(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.encript_password(form.cleaned_data['password'])
            usuario.save()
            context['success'] = 'Usuario registrado exitosamente'
            form = UserRegistrationForm()
        else:
            context['errors'] = form.errors
    else:
        form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'register.html', context)

def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            context['error'] = 'Username y password son requeridos'
            return render(request, 'login.html', context)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            context['error'] = 'Usuario o contraseña invalidos'
            return render(request, 'login.html', context)

        if not user.check_password(password):
            context['error'] = 'Usuario o contraseña invalidos'
            return render(request, 'login.html', context)


        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = user.id
        refresh['role'] = user.role
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        context['message'] = 'Login exitoso'
        context['role'] = user.role
        context['access_token'] = access_token
        context['refresh_token'] = refresh_token

        if user.role in ('user', 'docente'):
            return render(request, 'dashboard_blank.html', context)
        elif user.role == 'gestor_TI':
            return redirect(f'/api/panel_ti/politicas/?token={access_token}')

    return render(request, 'login.html', context)

def logout(request):
    if request.method == 'POST':
        refresh_token = request.POST.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
    return redirect('/api/auth/login/')
    

    
