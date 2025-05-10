from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import CreateView
from users.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from django.urls import reverse

class LoginFormView(LoginView):
    template_name = 'auth/login.html'
    success_url = 'private:home'  # Nombre de la URL definida en urls.py.

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirigir si el usuario ya está autenticado
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if not self.success_url:
            raise ValueError("No se ha configurado 'success_url'.")
        messages.success(self.request, 'Se ha iniciado sesión correctamente.')
        return reverse(self.success_url)

    def form_invalid(self, form):
        email = form.cleaned_data.get('username')  # Obtener el email o username del formulario
        password = form.cleaned_data.get('password')  # Obtener la contraseña del formulario

        try:
            user = User.objects.get(email=email)  # Busca al usuario por su username
        except User.DoesNotExist:
            # El usuario no existe
            messages.error(self.request, 'El usuario no existe.')
            return super().form_invalid(form)

        if not user.is_active:
            # El usuario está inactivo
            messages.error(self.request, 'Su cuenta está desactivada. Comuníquese con un administrador.')
        else:
            # Comprobar si la contraseña es incorrecta
            user_auth = authenticate(self.request, email=email, password=password)

            if user_auth is None:
                messages.error(self.request, 'La contraseña es incorrecta.')

        return super().form_invalid(form)

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        # Guarda el usuario
        user = form.save()

        # Pasar el backend como string
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')  # Especificar el backend correcto como un string

        messages.success(self.request, 'Usuario registrado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mensajes de error más específicos
        if 'email' in form.errors:
            messages.error(self.request, form.errors['email'][0])  # Error del campo email
        elif 'password2' in form.errors:
            messages.error(self.request, form.errors['password2'][0])  # Error de contraseñas
        else:
            messages.error(self.request, 'Error al registrar el usuario. Asegúrate de que los campos sean válidos.')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        # Redirige si el usuario ya está autenticado
        if request.user.is_authenticated:
            return redirect(reverse('private:home'))
        return super().dispatch(request, *args, **kwargs)
    
class LogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('auth:login') 

def link_logout(request):
    logout(request)
    return redirect('public:home')