from django.urls import path
from .views import EmployeeListView
app_name = 'employee'

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
]