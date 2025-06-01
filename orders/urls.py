

from django.urls import path, include
from .views import *
app_name = 'orders'
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', OrderListView.as_view(), name='list'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='detail'),

]

