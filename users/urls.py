from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserSoftDeleteView, UserDetailView
app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('crear/', UserCreateView.as_view(), name='create'),
    path('<str:pk>/', UserDetailView.as_view(), name='view'),
    path('<str:pk>/editar/', UserUpdateView.as_view(), name='update'),
    path('<str:pk>/desactivar/', UserSoftDeleteView, name='desactivar'),
]
