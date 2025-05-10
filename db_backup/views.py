from django.conf import settings
from django.http import FileResponse
from pathlib import Path
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required


class DatabaseBackupView(LoginRequiredMixin, ValidatePermissionRequiredMixin,  TemplateView):
    template_name = 'db_backup/db_backup.html'
    permission_required = ['private.change_configuration']

@login_required
@permission_required('private.change_configuration', raise_exception=True)
def export_database(request):
    # Ruta del archivo de la base de datos
    database_path = Path(settings.BASE_DIR).joinpath('db.sqlite3')
    
    # Verifica si el archivo existe
    if os.path.exists(database_path):
        # Obtener la fecha y hora actual en el formato deseado
        current_time = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
        
        # Crear el nombre del archivo de backup con la fecha y hora
        backup_filename = f"backup_{current_time}.sqlite"
        
        # Crear la respuesta con el archivo de backup
        response = FileResponse(open(database_path, 'rb'))
        
        # Establecer el encabezado para la descarga, incluyendo el nombre del archivo con la fecha
        response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
        
        # Retornar la respuesta de descarga
        return response
    
    # Si la base de datos no existe, usar messages.error para mostrar un error
    messages.error(request, 'Archivo de base de datos no encontrado.')
    
    # Redirigir a la vista de backups
    return redirect('backup:db_backup') 

@login_required
@permission_required('private.change_configuration', raise_exception=True)
def import_database(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_path = Path(settings.BASE_DIR).joinpath('db.sqlite3')

        # Guarda el archivo subido como la nueva base de datos
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Mensaje de éxito usando messages.success
        messages.success(request, 'Base de datos importada correctamente.')

        # Redirige a una vista donde el mensaje se pueda mostrar
        return redirect('backup:db_backup')  # Cambia 'home' por la URL de tu página de inicio o vista correspondiente

    # Si no se pudo importar la base de datos, mostrar un mensaje de error
    messages.error(request, 'Error al importar la base de datos.')
    
    # Redirige a la misma página o a una página de error
    return redirect('backup:db_backup') 