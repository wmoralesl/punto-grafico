from django.shortcuts import render
from .models import Employee
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView
from .forms import EmployeeForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy

# Create your views here.

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.all().order_by('id')
    
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