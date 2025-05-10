from .forms import UserUpdateForm
from .models import User
from authentication.forms import CustomUserCreationForm
from authentication.mixins import ValidatePermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from private.utils import log_user_action, get_client_ip

User = get_user_model()

# Lista de usuarios
class UserListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = ['users.view_user']
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    raise_exception = False
    paginate_by = 10
    order_by = 'username'

    def apply_filters(self, queryset):
        query = self.request.GET.get("q")
        if query:
            filters = (
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(second_last_name__icontains=query)
        )
            queryset = queryset.filter(filters)
        return queryset.filter(is_active=True)

    def get_queryset(self):
        return self.apply_filters(super().get_queryset())

# Crear usuario
class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ['users.add_user']
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_formCreate.html'
    success_url = reverse_lazy('users:list')
    raise_exception = False

    def form_valid(self, form):
        response = super().form_valid(form)  # Guarda el nuevo usuario
        
        # Registrar la acción del usuario
        log_user_action(
            user=self.request.user,
            action="Registró un nuevo usuario",
            model_name="User",
            object_id=str(self.object.id),  # El ID del usuario recién creado
            ip_address=get_client_ip(self.request),
        )
        
        messages.success(self.request, 'Usuario creado exitosamente.', extra_tags='success')
        return response

    def form_invalid(self, form):
        # Mensajes personalizados según el campo con errores
        if 'email' in form.errors:
            for error in form.errors['email']:
                if "already exists" in error:
                    messages.error(self.request, 'El correo ya está registrado.', extra_tags='error')
                elif "inactive" in error:
                    messages.error(self.request, 'El correo está inactivo.', extra_tags='error')
                else:
                    messages.error(self.request, error)

        if 'password2' in form.errors:
            for error in form.errors['password2']:
                if "do not match" in error:
                    messages.error(self.request, 'Las contraseñas no coinciden.', extra_tags='error')
                else:
                    messages.error(self.request, 'Error en la contraseña: ' + error)

        if 'password1' in form.errors:
            for error in form.errors['password1']:
                messages.error(self.request, 'Error en la contraseña: ' + error)

        # Mensaje genérico en caso de otros errores
        if not form.errors:
            messages.error(self.request, 'No fue posible crear el usuario.', extra_tags='error')

        return super().form_invalid(form)

# Editar usuario
class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm  # Cambia 'fields' por 'form_class'
    permission_required = ['users.change_user']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')
    raise_exception = False

    def form_valid(self, form):
        log_user_action(
            user=self.request.user,
            action="Editó la configuración de usuario",
            model_name="User",
            object_id=str(self.object.id),
            ip_address=get_client_ip(self.request),
            additional_info={"updated_fields": form.changed_data}
        )
        messages.success(self.request, 'Usuario actualizado exitosamente.', extra_tags='success')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('users:view', kwargs={'pk': self.object.id})

@login_required
@permission_required(['users.delete_user', 'users.change_user'], raise_exception=True)
def UserSoftDeleteView(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

    usuario = get_object_or_404(User, pk=pk)

    if usuario.is_superuser:
        messages.error(request, 'No puedes eliminar un usuario superadministrador.', extra_tags='error')
        return redirect('users:view', pk=usuario.id)
    
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.', extra_tags='error')
        return redirect('users:view', pk=usuario.id)
    
    if usuario.role == 'admin':
        messages.error(request, 'No puedes eliminar un usuario administrador.', extra_tags='error')
        return redirect('users:view', pk=usuario.id)

    usuario.soft_delete()
    log_user_action(
        user=request.user,
        action="Desactivó un usuario",
        model_name="User",
        object_id=str(usuario.id),
        ip_address=get_client_ip(request),
        additional_info={
            "email": usuario.email,
            "username": usuario.username,
            "deleted_at": now().isoformat()  # Registrar cuándo se desactivó
        }
    )
    messages.success(request, f"El usuario {usuario.email} ha sido eliminado correctamente.")
    return redirect('users:list')

class UserDetailView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DetailView):
    model = User
    permission_required = ['users.view_user']
    template_name = 'users/user_detail.html'
    raise_exception = False
    context_object_name = 'user'
