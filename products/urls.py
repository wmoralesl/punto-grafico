

from django.urls import path
from .views import *
app_name = 'products'

urlpatterns = [
    path('catalogo/d/<str:public>/', DesignDetailView.as_view(), name='design_detail'),
    path('admin/d/', DesignListView.as_view(), name='design_list'),
    path('admin/d/create/', DesignCreateView.as_view(), name='design_create'),
    path('admin/d/update/<str:pk>/', DesignUpdateView.as_view(), name='design_update')
]
