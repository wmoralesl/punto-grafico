from django.urls import path
from .views import *

app_name = 'public' 

urlpatterns = [
    path('', HomePageViewPublic.as_view(), name='home'),
    path('catalogo/', CatalogPageViewPublic.as_view(), name='catalog'),
    path('nosotros/', AboutUsPageViewPublic.as_view(), name='about_us'),
    path('preguntas/', QuestionPageViewPublic.as_view(), name='questions'),
]
