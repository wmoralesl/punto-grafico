from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Client
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import ClientForm
from django.contrib import messages
from django.db.models import Q

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def apply_filters(self, queryset):
        query = self.request.GET.get("q")
        if query:
            filters = (
            Q(name__icontains=query) |
            Q(phone__icontains=query) 
        )
            queryset = queryset.filter(filters)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.apply_filters(queryset)
        return queryset.order_by('-created')

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'clients/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients:client_list')
    raise_exception = False

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear el cliente. Por favor, verifica los datos ingresados.", extra_tags='error')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente creado exitosamente.", extra_tags='success')
        return super().form_valid(form)

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'
    raise_exception = False

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'clients/client_form.html'
    form_class = ClientForm

    def get_success_url(self):
        messages.success(self.request, "Cliente actualizado exitosamente.", extra_tags='success')
        return reverse('clients:client_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar el cliente. Por favor, verifica los datos ingresados.", extra_tags='error')
        return super().form_invalid(form)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_delete.html'
    raise_exception = False

    
    def get_success_url(self):
        messages.success(self.request, "Cliente eliminado exitosamente.", extra_tags='success')
        return reverse('clients:client_list')
