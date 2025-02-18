import json
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Creneau, RendezVous
from django.http import JsonResponse
from django.contrib.auth import login , logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RendezVousForm
from .forms import RegistrationForm
from django.urls import reverse
from django.core.serializers import serialize

# Create your views here.

def inscription_view(request):
    # Si tu utilises un formulaire d'inscription, crée-le ici.
    return render(request, 'registration/registration.html')


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Rediriger l'utilisateur vers la page de connexion après inscription
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mes_rdv')  # Redirige l'utilisateur après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def liste_creneaux(request):
    # Récupère tous les créneaux, sans filtrer par disponibilité
    creneaux = Creneau.objects.all()

    if not creneaux:
        message = "Aucun créneau disponible actuellement."
    else:
        message = "Voici les créneaux disponibles."

    return render(request, 'reservations/liste_creneaux.html', {'creneaux': creneaux, 'message': message})


@login_required
def reserver_rdv(request, id):
    creneau = get_object_or_404(Creneau, id=id)

    # Vérifie si le créneau est déjà réservé
    if not creneau.disponible:
        return redirect('liste_creneaux')  # Redirige si le créneau est déjà réservé

    # Si le créneau est disponible, crée la réservation
    if request.method == 'POST':
        RendezVous.objects.create(
            user=request.user,
            creneau=creneau
        )

        # Marquer le créneau comme non disponible
        creneau.disponible = False
        creneau.save()

        return redirect('liste_creneaux')  # Redirige vers la liste des créneaux

    return render(request, 'reservations/reserver.html', {'creneau': creneau})

@login_required
def mes_rdv(request):
    
    # Vérifie si l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return redirect('login')  # Rediriger vers la page de connexion si non authentifié

    # Récupère les rendez-vous de l'utilisateur connecté
    rdvs = RendezVous.objects.filter(user=request.user)

    # Affiche un message si l'utilisateur n'a pas de rendez-vous
    if not rdvs:
        message = "Vous n'avez aucun rendez-vous réservé."
    else:
        message = "Voici vos rendez-vous réservés."

    return render(request, 'reservations/mes_rdv.html', {'rdvs': rdvs, 'message': message})

@login_required
def api_creneaux(request):
    creneaux = Creneau.objects.filter(disponible=True)
    data = [
        {
            'id': creneaux.id,
            'title': creneaux.titre,
            'start': creneaux.start_time.isoformat(),
            'end': creneaux.end_time.isoformat(),
            'color': 'green' if creneaux.disponible else 'red',  # Utilisation de la propriété `color`
        }
        for c in creneaux
    ]
    return JsonResponse(data, safe=False)



def calendrier(request):
    # Récupérer tous les créneaux
    creneaux = Creneau.objects.all()

    # Créer une liste d'événements formatés pour FullCalendar
    events = [
        {
            'id': creneau.id,
            'title': creneau.titre,
            'start': creneau.start_time.isoformat(),
            'end': creneau.end_time.isoformat(),
            'color': 'green' if creneau.disponible else 'red',
            'url': reverse('reserver_rdv', args=[creneau.id])  # Lien vers la page de réservation
        }
        for creneau in creneaux
    ]

    # Sérialiser les événements en JSON
    events_json = json.dumps(events) if events else '[]'  # Assurez-vous que c'est un tableau JSON valide
    
    return render(request, 'reservations/calendrier.html', {'events_json': events_json})

def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return render(request, 'reservations/logout.html')  # Affiche la page de déconnexion