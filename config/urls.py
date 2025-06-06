"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import handler404, handler403
from public.views import custom_404_view, custom_403_view

handler404 = custom_404_view
handler403 = custom_403_view

urlpatterns = [
    path('', include("public.urls")), 
    path('', include("products.urls")),
    path('auth/', include("authentication.urls")), 
    path('admin/', include([
        path('', include("private.urls")),
        path('u/', include("users.urls")),
        path('config/backup/', include("db_backup.urls")),
        path('o/', include("orders.urls")),
        path('c/', include("clients.urls")),
        path('e/', include("employee.urls")),
    ])),
    path('super/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
