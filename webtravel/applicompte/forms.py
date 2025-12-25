from django.forms import ModelForm
from applicompte.models import TravelUser

class TravelUserForm(ModelForm) : 
    class Meta :
        model = TravelUser
        fields = ['username', 'first_name', 'last_name', 'email', 'image']
        