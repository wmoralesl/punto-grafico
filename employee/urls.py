from django.urls import path
from .views import EmployeeListView, EmployeeDetailView
app_name = 'employee'

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
]