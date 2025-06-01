from django.shortcuts import render
from .models import Employee
from django.views.generic import ListView
# Create your views here.

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Employee.objects.all().order_by('name')