from django.urls import path
from .views import EmployeeListView, EmployeeDetailView, EmployeeUpdateView, EmployeeCreateView
app_name = 'employee'

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),

]