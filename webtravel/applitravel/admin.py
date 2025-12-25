from django.contrib import admin

# Register your models here.
from applitravel.models import Ville, Voyage, Etape
admin.site.register(Ville)
admin.site.register(Voyage)
admin.site.register(Etape)