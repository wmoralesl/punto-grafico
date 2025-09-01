from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from .forms import OrderForm, OrderLineFormSet, OrderUpdateForm, OrderLineForm
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView, DetailView, ListView, View, UpdateView, DeleteView, CreateView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from config import settings
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Client, Order, OrderLine, OrderStatus
from .serializers import ClientSerializer, OrderSerializer, OrderDetailSerializer, OrderLineSerializer, EmployeeSerializer
from employee.models import Employee
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import smart_str
from .untils import printPDF
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from weasyprint import HTML
from urllib.parse import quote

# Create your views here.

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def apply_filters(self, queryset):
        query = self.request.GET.get("q")
        if query:
            filters = (
                Q(client__name__icontains=query) |
                Q(client__phone__icontains=query) |
                Q(lines__description__icontains=query)
            )
            queryset = queryset.filter(filters).distinct()
        return queryset
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.apply_filters(queryset)
        # Ordenar por fecha de creación descendente
        return queryset.order_by('-created')
    
    def get_context_data(self, **kwargs):
        # Mostrar la cantidad de resultados
        context = super().get_context_data(**kwargs)
        context['total_orders'] = self.get_queryset().count()
        return context 

class OrderCreateView(TemplateView):
    template_name = 'orders/order_create.html'

class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'orders/order_update.html'
    form_class = OrderUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Pedido actualizado exitosamente.')
        return reverse('orders:detail', kwargs={'pk': self.object.pk})


class OrderDetailView(DetailView):
    template_name = 'orders/order_detail.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = OrderStatus.objects.all().order_by('id')  # o por un campo como 'code'
        return context

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['position', 'is_working']

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

class ChangeOrderStatusView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status_code = request.POST.get('status')  # viene del template

        if not new_status_code:
            messages.error(request, "No se especificó el nuevo estado.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            new_status = OrderStatus.objects.get(code=new_status_code)
            order.current_status = new_status
            order.save(update_fields=['current_status'])
            messages.success(request, f"Estado cambiado a: {new_status}")
        except OrderStatus.DoesNotExist:
            messages.error(request, "Estado inválido.")

        return redirect(request.META.get('HTTP_REFERER', '/'))
# ********************************************* Imprimir Orden ************************

class OrderPrintView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        
        orden = get_object_or_404(Order, pk=pk)
        css_url = finders.find('css/general.css')
        html_name = 'print/orderPrint.html'

        data = {
            'order': orden,

        }
        pdf = printPDF(html_name, css_url, data)
        response = HttpResponse(pdf, content_type='application/pdf')
        nombre_archivo = "Mipedido.pdf"
        response['Content-Disposition'] = f"inline; filename*=UTF-8''{quote(nombre_archivo)}"
        
        # response['Content-Disposition'] = 'attachment; filename="pedido.pdf"'
        return response

class OrderPreviewPrint(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'print/orderPrint.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['css_url'] = finders.find('css/general.css')
        return context
    
# ******************************************** Client ************************

# Client sugestion
class ClientSuggestionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            term = request.GET.get('term', '')
            clientes = Client.objects.filter(Q(name__icontains=term) | Q(phone__icontains=term))
            results = [{'id': cliente.id, 'name': cliente.name, 'phone': cliente.phone} for cliente in clientes]
            return JsonResponse(results, safe=False)
        return JsonResponse([], safe=False)
    
# ************************************************ Lineas ***********************************************************

class OrderLineUpdateView(UpdateView):
    model = OrderLine
    template_name = 'lines/orderline_update.html'
    form_class = OrderLineForm


    def get_success_url(self):
        messages.success(self.request, 'Línea de pedido actualizada exitosamente.')
        return reverse('orders:detail', kwargs={'pk': self.object.order.pk})

class OrderLineDeleteView(DeleteView):
    model = OrderLine
    template_name = 'lines/orderline_delete.html'
    context_object_name = 'orderline'

    def get_success_url(self):
        messages.success(self.request, 'Línea de pedido eliminada exitosamente.')
        return reverse('orders:detail', kwargs={'pk': self.object.order.pk})
    
class OrderLineCreateView(CreateView):
    model = OrderLine
    template_name = 'lines/orderline_create.html'
    form_class = OrderLineForm

    def form_valid(self, form):
        # Obtener el pedido al que se asociará esta línea
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        form.instance.order = order
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Línea de pedido creada exitosamente.')
        return reverse('orders:detail', kwargs={'pk': self.object.order.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, pk=self.kwargs['pk'])
        return context