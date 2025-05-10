from django.urls import path
from . import views

app_name = 'backup'

urlpatterns = [
    path('', views.DatabaseBackupView.as_view(), name='db_backup'),
    path('export/', views.export_database, name='export_database'),
    path('import/', views.import_database, name='import_database'),
]
