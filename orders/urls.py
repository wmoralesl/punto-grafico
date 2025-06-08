

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
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='update'),

    path('update/line/<int:pk>/', OrderLineUpdateView.as_view(), name='update-line'),
    path('delete/line/<int:pk>/', OrderLineDeleteView.as_view(), name='delete-line'),
    path('create/line/<int:pk>/', OrderLineCreateView.as_view(), name='create-line'),
    
    path('client-suggestions/', ClientSuggestionsView.as_view(), name='client-suggestions'),


]

