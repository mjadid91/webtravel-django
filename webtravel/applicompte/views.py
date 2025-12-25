from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from applitravel.models import Voyage
from applicompte.models import TravelUser
from applicompte.forms import TravelUserForm

# Create your views here.
def connexion(request):
    # securisation : interdit pour client/staff connecté
    # Le formulaire de connexion est interdit pour un utilisateur déjà connecté
    if request.user.is_authenticated:
        # Client ou Staff déjà connecté: on le redirige vers la liste des voyages
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, "user": user}
        )

    # internaute non connecté (autorisé à tenter la connexion)
    usr = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(request, username=usr, password=pwd)

    if user is not None:
        login(request, user)
        lesVoyages = Voyage.objects.all()
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, "user": user}
        )
    else:
        return render(
            request,
            'applicompte/login.html'
        )

def deconnexion(request):
    logout(request)
    return render(
        request,
        'applicompte/logout.html'
    )

def formulaireProfil(request):
    user = None
    if request.user.is_authenticated:
        user = TravelUser.objects.get(id = request.user.id)
        return render (
            request,
            'applicompte/profil.html',
            {"user" : user}
        )

    else : 
        return render(
            request,
            'applicompte/login.html'
        )

def traitementFormulaireProfil(request):
    user = None

    if request.user.is_authenticated : 
        user = TravelUser.objects.get(id = request.user.id)
        form = TravelUserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            user = TravelUser.objects.get(id = request.user.id)
        lesVoyages = Voyage.objects.all()
        return render (
            request,
            'applitravel/voyages.html',
            {"voyages" : lesVoyages, "user" : user}
        )
    else :
        return render(
            request,
            'applicompte/login.html'
        )

def formulaireInscription(request):
    return render(
        request,
        'applicompte/formulaireInscription.html'
    )

def traitementFormulaireInscription(request):
    prenom = request.POST['first_name']
    nom = request.POST['last_name']
    usr = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    img = request.POST['image']

    user = TravelUser()

    user.first_name = prenom
    user.last_name = nom
    user.username = usr 
    user.email = email
    user.set_password(password)
    user.image = img

    user.save()

    login(request, user)
    lesVoyages = Voyage.objects.all()

    return render(
        request,
        'applitravel/voyages.html',
        {"voyages" : lesVoyages, "user" : user}
    )
