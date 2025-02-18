from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.liste_creneaux, name='liste_creneaux'),
    path('calendrier/', views.calendrier, name='calendrier'),
    path('inscription/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/creneaux/', views.api_creneaux, name='api_creneaux'),
    path('reserver/<int:id>/', views.reserver_rdv, name='reserver_rdv'),
    path('mes_rdv/', views.mes_rdv, name='mes_rdv'),
]
         