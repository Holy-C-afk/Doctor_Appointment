
from django.contrib import admin
from .models import Medecin, Creneau, RendezVous

# Register your models here.


admin.site.register(Medecin)
admin.site.register(Creneau)
admin.site.register(RendezVous)
