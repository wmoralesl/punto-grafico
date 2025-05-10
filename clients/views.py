from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Client

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10