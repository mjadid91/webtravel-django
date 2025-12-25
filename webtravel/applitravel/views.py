from django.shortcuts import render
from applitravel.models import Voyage, Ville, Etape
from applitravel.forms import VilleForm, VoyageForm, EtapeForm
from django.http import HttpResponse
from django.template import loader
from applicompte.models import TravelUser


# Create your views here.
def main(request):
  template = loader.get_template('applitravel/main.html')
  return HttpResponse(template.render())

def voyages(request):
    user = None
    if request.user.is_authenticated : 
        user = TravelUser.objects.get(id = request.user.id)

    lesVoyages = Voyage.objects.all()
    return render (
        request, 
        'applitravel/voyages.html',
        {'voyages': lesVoyages, 'user': user},
    )

def villes(request):
    user = None

    # user staff
    if request.user.is_staff : 
        lesVilles = Ville.objects.all()
        user = TravelUser.objects.get(id = request.user.id)
        return render (
            request,
            'applitravel/villes.html',
            {'villes': lesVilles, 'user': user}
        )

    # client connecté
    if request.user.is_authenticated : 
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id = request.user.id)
        return render (
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )

    # internaute non connecté
    else:
        return render (
            request, 
            'applicompte/login.html',
        )

def voyage(request, voyage_id):
    user = None
    # On recupere le voyage à l'aide de l'ID qu'on passe en parametre de cette fonction
    leVoyage = Voyage.objects.get(IDVoyage=voyage_id)
    lesEtapes = Etape.objects.filter(voyage = voyage_id)
    # modifie la vue voyage en recuperant toute les villes
    lesVilles = Ville.objects.all()

    if request.user.is_authenticated : 
        user = TravelUser.objects.get(id = request.user.id)

    # on retourne le template voyage.html avec le voyage
    return render(
        request, 
        'applitravel/voyage.html', 
        {'voyage': leVoyage, 'etapes': lesEtapes, 'villes': lesVilles, 'user': user}
    )

def formulaireCreationVille(request):
    # user staff
    if request.user.is_staff :
        form = VilleForm()
        # on retourne l'emplacement du template
        return render (
            request,
            'applitravel/formulaireCreationVille.html',
            {'form' : form}
        )
    if request.user.is_authenticated :
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id = request.user.id)
        return render (
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    # internaute non connecté (interdit)
    else:
        return render(
            request,
            'applicompte/login.html',
        )
        
def CreerVille(request) :
    if request.user.is_staff:
        # on récupere le formulaire
        form = VilleForm(request.POST)
        # test de la validité du formulaire
        if form.is_valid() :
            nomV = form.cleaned_data['NomVille']
            # on sauvegarde dans la base
            form.save()

        return render(
            request,
            'applitravel/traitementFormulaireCreationVille.html',
            {"nom": nomV}
        )
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id = request.user.id)
        return render (
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def formulaireCreationVoyage(request):
    if request.user.is_staff :
        form = VoyageForm()
        return render(
            request,
            'applitravel/formulaireCreationVoyage.html',
            {'form' : form}
        )
    # client connecté (interdit)
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    # internaute non connecté (interdit)
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def CreerVoyage(request) :
    if request.user.is_staff:
        form = VoyageForm(request.POST, request.FILES) # request.FILES sert a prendre en compte la gestion de fichiers
        if form.is_valid() :
            titreVoy = form.cleaned_data['Titre']
            prixVoy = form.cleaned_data['Prix']
            form.save()

        return render(
            request,
            'applitravel/traitementFormulaireCreationVoyage.html',
            {"titre": titreVoy, "prix": prixVoy}
        )
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def ajouterEtape(request, IDVoyage) :
    if request.user.is_staff:
        form = EtapeForm(request.POST)
        if form.is_valid() :
            vil = form.cleaned_data['ville']
            nbjours = form.cleaned_data['Nb_jours']
            voy = Voyage.objects.get(IDVoyage = IDVoyage)
            lesEtapes = Etape.objects.filter(voyage = IDVoyage)
            lesEtapesduvoyage = ((ligne.ville) for ligne in lesEtapes)

            # on supp l'étape si elle existe déjà
            if vil in lesEtapesduvoyage :
                eta = Etape.objects.filter(voyage = voy, ville = vil)
                eta.delete()

            newEtape = Etape()
            newEtape.ville = vil
            newEtape.voyage = voy
            newEtape.Nb_jours = nbjours
            newEtape.save()

        leVoyage = Voyage.objects.get(IDVoyage = IDVoyage)
        lesEtapes = Etape.objects.all().filter(voyage = leVoyage)
        lesVilles = Ville.objects.all()

        return render (
            request,
            'applitravel/voyage.html',
            {'voyage': leVoyage, 'etapes' : lesEtapes, 'lesVilles' : lesVilles}
        )
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def supprimerVoyage(request, voyage_id) :
    if request.user.is_staff:
        leVoyage = Voyage.objects.get(IDVoyage=voyage_id)
        leVoyage.delete()
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def afficherFormulaireModificationVoyage(request, voyage_id):
    if request.user.is_staff :
        # on recupere le voyage dont l'ID a ete recuperer en parametre
        leVoyage = Voyage.objects.get(IDVoyage = voyage_id)
        return render (
            request,
            'applitravel/formulaireModificationVoyage.html',
            {"voyage" : leVoyage }
        )

    if request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )

    else:
        return render(
            request,
            'applicompte/login.html',
        )

def modifierVoyage(request, voyage_id):
    if request.user.is_staff:
        leVoyage = Voyage.objects.get(IDVoyage=voyage_id)
        form = VoyageForm(request.POST, request.FILES, instance=leVoyage)

        if form.is_valid():
            titreVoy = form.cleaned_data['Titre']
            prixVoy = form.cleaned_data['Prix']
            form.save()

        return render(
            request,
            'applitravel/traitementFormulaireModificationVoyage.html',
            {"titre": titreVoy, "prix": prixVoy}
        )
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def supprimerVille(request, ville_id) :
    if request.user.is_staff:
        laVille = Ville.objects.get(IDVille = ville_id)
        laVille.delete()
        lesVilles = Ville.objects.all()
        return render(
            request,
            'applitravel/villes.html',
            {'villes': lesVilles}
        )
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def afficherFormulaireModificationVille(request, ville_id):

    if request.user.is_staff :
        # on recupere le voyage dont l'ID a ete recuperer en parametre
        laVille = Ville.objects.get(IDVille = ville_id)
        return render (
            request,
            'applitravel/formulaireModificationVille.html',
            {"ville" : laVille }
        )

    # client connecté
    if request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )

    # internaute non connecté
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def modifierVille(request, ville_id):
    if request.user.is_staff:
        laVille = Ville.objects.get(IDVille=ville_id)
        form = VilleForm(request.POST, instance=laVille)
        if form.is_valid():
            nomVille = form.cleaned_data['NomVille']
            nomPays = form.cleaned_data['NomPays']
            form.save()

        return render(
            request,
            'applitravel/traitementFormulaireModificationVille.html',
            {"ville": nomVille, "pays": nomPays}
        )

    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def supprimerEtapeDansVoyage (request, voyage_id, etape_id):
    if request.user.is_staff:
        uneEtape = Etape.objects.get(IDEtape=etape_id)
        uneEtape.delete()

        unVoyage = Voyage.objects.get(IDVoyage=voyage_id)
        lesEtapes = Etape.objects.filter(voyage=unVoyage)

        lesEtapesduvoyage = ((ligne.ville) for ligne in lesEtapes)
        lesVilles = Ville.objects.all()

        return render(
            request,
            'applitravel/voyage.html',
            {'voyage': unVoyage, 'etapes': lesEtapes, 'villes': lesVilles}
        )
    elif request.user.is_authenticated:
        lesVoyages = Voyage.objects.all()
        user = TravelUser.objects.get(id=request.user.id)
        return render(
            request,
            'applitravel/voyages.html',
            {'voyages': lesVoyages, 'user': user}
        )
    else:
        return render(
            request,
            'applicompte/login.html',
        )

def modifierEtapeDansVoyage (request, voyage_id, etape_id):
    uneEtape = Etape.objects.get(IDEtape=etape_id)
    form = EtapeForm(request.POST, instance=uneEtape)
    if form.is_valid():
        vil = form.cleaned_data['ville']
        nbjours = form.cleaned_data['Nb_jours']
        voy = Voyage.objects.get(IDVoyage=voyage_id) # on recup le voyage qui appartient a cette etape

        # on supp l'etape et on reconstruit completement
        uneEtape.delete()
        newEtape = Etape()
        newEtape.ville = vil
        newEtape.voyage = voy
        newEtape.Nb_jours = nbjours
        newEtape.save()

    leVoyage = Voyage.objects.get(IDVoyage = voyage_id) # on recup encore le voyage car est liée a l'etape en question
    lesEtapes = Etape.objects.all().filter(voyage = leVoyage) # donne toutes les étapes qui appartiennent au voyage

    return render(
        request,
        'applitravel/traitementFormulaireModificationEtape.html',
        {"etape": uneEtape}
    )

def afficherFormulaireModificationEtape(request, voyage_id, etape_id):
    uneEtape = Etape.objects.get(IDEtape=etape_id) # on recup l'etape
    lesVilles = Ville.objects.all()  # récupère toutes les villes

    leVoyage = Voyage.objects.get(IDVoyage=voyage_id) # on recup le voyage

    return render(
        request,
        'applitravel/formulaireModificationEtape.html',
        {
            "etape": uneEtape,
            "voyage": leVoyage,
            "villes": lesVilles
        }
    )

