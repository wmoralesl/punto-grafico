from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Configuration, UserActionLog
from .forms import ConfigurationForm, CustomPasswordChangeForm, MyProfileForm
from authentication.mixins import ValidatePermissionRequiredMixin
from django.contrib import messages
from users.models import User
from orders.models import Order
from clients.models import Client
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date, timedelta
from django.db.models import Q
from .graphs import lastTwelveMonths, lastTwelveMonthsName
import json
from .utils import log_user_action, get_client_ip

# Create your views here.

class HomeViewPrivate(LoginRequiredMixin, TemplateView):
    template_name =  'private/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Current_date = date.today()
        Current_month = Current_date.month
        Current_year = Current_date.year

        all_orders = Order.objects.count()
        all_clients = Client.objects.count()

        orders_this_month = Order.objects.filter(Q(request_date__month=Current_month) & Q(request_date__year=Current_year)).count()
        clients_this_month = Client.objects.filter(Q(created__month=Current_month) & Q(created__year=Current_year)).count()

        orders_this_day = Order.objects.filter(Q(request_date=Current_date))
        delivery_now = Order.objects.filter(deadline=Current_date)  # Pedidos entregados hoy
        delivery_tomorrow = Order.objects.filter(deadline=Current_date + timedelta(days=1))  # Pedidos a entregar mañana
        
        clients_data = lastTwelveMonths(Client, "clientes", Current_date)
        orders_data = lastTwelveMonths(Order, "orders", Current_date)
        months_name = lastTwelveMonthsName(Current_date)


        user = self.request.user
        if user.is_authenticated:
            context['user_permissions'] = user.get_all_permissions()
        else:
            context['user_permissions'] = set()  # Usuario no autenticado

        context['all_orders'] = all_orders
        context['all_clients'] = all_clients
        context['orders_this_month'] = orders_this_month
        context['clients_this_month'] = clients_this_month
        context['orders_this_day'] = orders_this_day
        context['delivery_now'] = delivery_now
        context['delivery_tomorrow'] = delivery_tomorrow
        context['clients_data'] = json.dumps(clients_data)
        context['orders_data'] = json.dumps(orders_data)
        context['months_name'] = json.dumps(months_name)
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
    

class calendarView(LoginRequiredMixin, TemplateView):
    template_name = 'private/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()

        # Crear eventos solo para órdenes
        events = [
            {
                'title': order.client.name,
                'start': order.deadline.strftime('%Y-%m-%d'),
                'end': order.deadline.strftime('%Y-%m-%d'),
                'url': reverse('orders:detail', kwargs={'pk': order.id}),
                'color': 'green' if order.current_status.code == "cancelado" else 'red',
            }
            for order in orders
        ]

        context['events'] = json.dumps(events)
        return context