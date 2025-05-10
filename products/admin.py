from django.contrib import admin
from .models import TShirt, Tag, Design
# Register your models here.

admin.site.register(TShirt)
admin.site.register(Tag)
admin.site.register(Design)
