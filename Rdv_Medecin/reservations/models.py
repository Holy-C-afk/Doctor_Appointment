from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medecin(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} - {self.specialite}"

class Creneau(models.Model):
    titre = models.CharField(max_length=255)  # Titre du créneau
    medecin = models.ForeignKey('Medecin', on_delete=models.CASCADE)  # Médecin associé
    start_time = models.DateTimeField()  # Heure de début
    end_time = models.DateTimeField()  # Heure de fin
    disponible = models.BooleanField(default=True)  # Disponibilité

    def __str__(self):
        return f"{self.titre} - {self.start_time} à {self.end_time}"

    @property
    def color(self):
        return 'green' if self.disponible else 'red'


class RendezVous(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV {self.user.username} avec {self.creneau.medecin.nom} le {self.creneau.start_time} à {self.creneau.end_time}"


