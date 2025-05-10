from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Configuration, UserActionLog
from .forms import ConfigurationForm, CustomPasswordChangeForm, MyProfileForm
from authentication.mixins import ValidatePermissionRequiredMixin
from django.contrib import messages
from users.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .utils import log_user_action, get_client_ip
# Create your views here.

class HomeViewPrivate(LoginRequiredMixin, TemplateView):
    template_name =  'private/main.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            context['user_permissions'] = user.get_all_permissions()
        else:
            context['user_permissions'] = set()  # Usuario no autenticado
        return context
    
class ConfigurationView(LoginRequiredMixin, TemplateView):
    template_name = 'private/organization/view_organization.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            configuration = Configuration.get_configuration()
        except Configuration.DoesNotExist:
            messages.error(self.request, "La configuración no existe. Contacta al administrador.", extra_tags='error')
            configuration = None
        context['configuration'] = configuration
        return context

class EditConfigurationView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = ['private.change_configuration']
    form_class = ConfigurationForm
    template_name = 'private/organization/update_organization.html'
    success_url = 'private:view_configuration'

    def get_object(self):
        # Asegúrate de que siempre se edite la misma configuración
        return Configuration.get_configuration()
    
    def get_success_url(self):
        if not self.success_url:
            raise ValueError("No se ha configurado 'success_url'.")
        messages.success(self.request, 'Cambios realizados exitosamente.', extra_tags='success')
        return reverse(self.success_url)

    def form_valid(self, form):
        response = super().form_valid(form)  # Procesar la actualización normalmente
        
        # Registrar la acción del usuario
        log_user_action(
            user=self.request.user,
            action="Editó la configuración de la organización",
            model_name="Configuration",
            object_id=str(self.object.id),
            ip_address=get_client_ip(self.request),
            additional_info={"updated_fields": form.changed_data}
        )
        
        return response

class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'private/profile/view_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = MyProfileForm
    template_name = 'private/profile/update_profile.html'
    success_url = reverse_lazy('private:view_profile')

    def get_object(self, queryset=None):
        # Retorna el usuario autenticado
        return self.request.user

    def form_valid(self, form):
        # Registrar la acción del usuario
        log_user_action(
            user=self.request.user,
            action="Editó la información de su perfil",
            model_name="User",
            object_id=str(self.object.id),
            ip_address=get_client_ip(self.request),
            additional_info={"updated_fields": form.changed_data}
        )
        messages.success(self.request, 'Usuario actualizado exitosamente.', extra_tags='success')
        return super().form_valid(form)

class BaseUserActionLogView(LoginRequiredMixin, ListView):
    model = UserActionLog
    context_object_name = 'actions'
    ordering = '-timestamp'

class MyUserActionLogView(BaseUserActionLogView):
    template_name = 'private/actions/my_action_logs.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)[:15]

class UserActionLogView(BaseUserActionLogView):
    template_name = 'private/actions/user_action_log.html'

    def get_queryset(self):
        return super().get_queryset()[:15]
      
class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'private/profile/update_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('private:view_profile')  # Redirige tras éxito
    success_message = "¡Tu contraseña ha sido cambiada con éxito!"

    def form_valid(self, form):
        # Lógica personalizada antes de guardar la nueva contraseña
        form.save(self.request.user)  # Usa el método save del formulario personalizado
        response = super().form_valid(form)
        print("Contraseña cambiada para el usuario:", self.request.user)
        return response
    

