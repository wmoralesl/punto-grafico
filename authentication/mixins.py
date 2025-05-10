from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request,*args, **kwargs)
        return redirect('public:home')

class ValidatePermissionRequiredMixin:
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Verificar si el usuario tiene todos los permisos requeridos
            if self.has_permissions():
                return super().dispatch(request, *args, **kwargs)
        
        # Mensaje de error y redirección si no tiene permiso
        messages.error(request, ' Acceso denegado', extra_tags='error')
        return redirect(self.get_url_redirect())
    
    def has_permissions(self):
        # Verificar que self.permission_required sea una lista o tupla
        if isinstance(self.permission_required, (list, tuple)):
            # Retornar True si el usuario tiene todos los permisos
            return all(self.request.user.has_perm(perm) for perm in self.permission_required)
        # Si solo es un permiso (cadena)
        return self.request.user.has_perm(self.permission_required)

    def get_url_redirect(self):
        return reverse('private:home')