from django.shortcuts import render
from .models import Employee
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView
from .forms import EmployeeForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Q
# Create your views here.

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'
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
        return self.apply_filters(super().get_queryset())
    
class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'
    raise_exception = False

class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employee/employee_form.html'
    form_class = EmployeeForm

    def get_success_url(self):
        messages.success(self.request, "Empleado actualizado exitosamente.", extra_tags='success')
        return reverse('employee:employee_detail', kwargs={'pk': self.object.pk})

class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'employee/employee_form.html'
    form_class = EmployeeForm

    def get_success_url(self):
        messages.success(self.request, "Empleado creado exitosamente.", extra_tags='success')
        return reverse('employee:employee_detail', kwargs={'pk': self.object.pk})
    
class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee/employee_delete.html'
    context_object_name = 'employee'

    def get_success_url(self):
        messages.success(self.request, "Empleado eliminado exitosamente.", extra_tags='success')
        return reverse_lazy('employee:employee_list')