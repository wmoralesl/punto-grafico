from django.shortcuts import render, redirect
from .forms import OrderForm, OrderLineFormSet
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView, DetailView, ListView, View

from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Client, Order, OrderLine
from .serializers import ClientSerializer, OrderSerializer, OrderDetailSerializer, OrderLineSerializer, EmployeeSerializer
from employee.models import Employee
# Create your views here.

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'


class OrderCreateView(TemplateView):
    template_name = 'orders/order_create.html'


class OrderDetailView(DetailView):
    template_name = 'orders/order_detail.html'
    model = Order
    context_object_name = 'order'

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name']

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['phone']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        order = serializer.save()
        # Calcular el total basado en las líneas
        lines = order.lines.all()
        total = sum(line.subtotal() for line in lines)
        order.total = total
        order.save()

# Client sugestion
class ClientSuggestionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            term = request.GET.get('term', '')
            clientes = Client.objects.filter(Q(name__icontains=term) | Q(phone__icontains=term))
            results = [{'id': cliente.id, 'name': cliente.name, 'phone': cliente.phone} for cliente in clientes]
            return JsonResponse(results, safe=False)
        return JsonResponse([], safe=False)