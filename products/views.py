from django.shortcuts import render, get_object_or_404
from .models import Design, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from private.utils import log_user_action, get_client_ip
from .forms import DesignForm
from django.contrib import messages
from django.db.models import Q

class DesignListView(ListView):
    model = Design
    template_name = 'products/design/private/design_list.html'
    context_object_name = 'playeras'
    paginate_by = 10

    def apply_filters(self, queryset):
        query = self.request.GET.get("q")
        if query:
            filters = (
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            )
            queryset = queryset.filter(filters).distinct()
        return queryset
    
    def get_queryset(self):
        return self.apply_filters(super().get_queryset())

class DesignDetailView(DetailView):
    model = Design
    template_name = 'products/design/public/design_detail.html'
    context_object_name = 'playera'


    def get_object(self):
        """ Obtiene el diseño por el campo 'public' en lugar de 'pk'. """
        return get_object_or_404(Design.objects.prefetch_related('tags'), public=self.kwargs['public'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_design = self.object  # El diseño actual (detalle)
        url_complete = self.request.build_absolute_uri()
        # Obtener los 3 diseños relacionados por categoría (tags)
        related_designs = Design.objects.filter(
            tags__in=current_design.tags.all()  # Diseños que compartan tags
        ).exclude(id=current_design.id).distinct()[:4]  # Excluir el diseño actual, limitar a 3

        # Agregar los diseños relacionados al contexto
        context['url_complete'] = url_complete
        context['related_designs'] = related_designs
        return context
    
class DesignCreateView(LoginRequiredMixin, CreateView):
    form_class = DesignForm
    template_name = 'products/design/private/design_create.html'
    success_url = reverse_lazy('products:design_list')
    raise_exception = False

    def form_valid(self, form):
        response = super().form_valid(form)  # Guarda el nuevo diseño
        
        # Registrar la acción del usuario
        log_user_action(
            user=self.request.user,
            action="Registró un nuevo diseño",
            model_name="Design",
            object_id=str(self.object.id),  # El ID del diseño recién creado
            ip_address=get_client_ip(self.request),
        )
        
        messages.success(self.request, 'Diseño creado exitosamente.', extra_tags='success')
        return response

    def form_invalid(self, form):
        if not form.errors:
            messages.error(self.request, 'No fue posible crear el diseño.', extra_tags='error')

        return super().form_invalid(form)
    
class DesignUpdateView(LoginRequiredMixin, UpdateView):
    model = Design
    form_class = DesignForm  
    permission_required = ['users.change_user']
    template_name = 'products/design/private/design_create.html'
    success_url = reverse_lazy('products:design_list')
    raise_exception = False

    def form_valid(self, form):
        log_user_action(
            user=self.request.user,
            action="Editó la informacion de diseño",
            model_name="Design",
            object_id=str(self.object.id),
            ip_address=get_client_ip(self.request),
            additional_info={"updated_fields": form.changed_data}
        )
        messages.success(self.request, 'Diseño actualizado exitosamente.', extra_tags='success')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('products:design_update', kwargs={'pk': self.object.id})
