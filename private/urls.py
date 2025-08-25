from django.urls import path
from .views import  HomeViewPrivate, EditConfigurationView, ConfigurationView, MyProfileView, EditProfileView, CustomPasswordChangeView, MyUserActionLogView, UserActionLogView, calendarView

app_name = 'private'

urlpatterns = [
     path('', HomeViewPrivate.as_view(), name='home'),
     path('config/', ConfigurationView.as_view(), name='view_configuration'),
     path('config/edit/', EditConfigurationView.as_view(), name='update_configuration'),
     path('config/actions/', UserActionLogView.as_view(), name = 'view_user_actions'),
     path('profile/', MyProfileView.as_view(), name='view_profile'),
     path('profile/actions/', MyUserActionLogView.as_view(), name = 'view_my_actions'),
     path('profile/edit/', EditProfileView.as_view(), name='update_profile'),
     path('profile/edit/password/', CustomPasswordChangeView.as_view(), name='update_password'),
     path('calendar/', calendarView.as_view(), name='calendar'),
]
