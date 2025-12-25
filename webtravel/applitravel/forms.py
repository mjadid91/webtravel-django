from django import forms
from django.forms import ModelForm
from applitravel.models import Ville, Voyage, Etape

class VilleForm(forms.ModelForm) :
    class Meta :
        model = Ville
        fields = ['NomVille', 'NomPays']
        labels = {
            'NomVille': 'Nom de la ville',
            'NomPays' : 'Nom du pays',
        }

class VoyageForm(forms.ModelForm) :
    class Meta :
        model = Voyage
        fields = ['Titre', 'Prix', 'image']
        labels = {
            'Titre' : 'Titre du voyage',
            'Prix' : 'Prix du voyage',
            'image' : 'Photo du voyage'
        }

class EtapeForm(forms.ModelForm):
    class Meta:
        model = Etape
        fields = ['ville', 'Nb_jours']
        labels = {
            'ville': 'Ville',
            'Nb_jours': 'Nombre de jours',
        }