from django.urls import path, include
from .views import LoginFormView, UserRegisterView, LogoutView, link_logout

app_name = 'auth'

urlpatterns = [
     path('login/', LoginFormView.as_view(), name='login'),
     # path('register/', UserRegisterView.as_view(), name='register'),
     # path('logout/', LogoutView.as_view(), name='logout'),
     path('logout/', link_logout, name='logout'),


]
