from django.db import models
from django.contrib.auth.models import User
from applitravel.models import Voyage 

class Commande(models.Model):
    IDCommande = models.AutoField(primary_key=True)
    DateCommande = models.DateField() 
    Payee = models.BooleanField()
    Prix = models.DecimalField(max_digits=8, decimal_places=2) 
    User_ID = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        null=True, 
        related_name="user_id"
    )

    def __str__(self) -> str:
        return self.IDCommande

class LigneCommande(models.Model):
    IDLigneCommande = models.AutoField(primary_key=True)
    Quantite = models.IntegerField()
    Prix = models.DecimalField(max_digits=8, decimal_places=2)

    # Lien vers la commande (Panier)
    Commande_ID = models.ForeignKey(
        Commande, 
        on_delete=models.CASCADE, 
        related_name="ID_Commande"
    )
    
    # Lien vers le voyage
    Voyage_ID = models.ForeignKey(
        Voyage, 
        on_delete=models.DO_NOTHING, 
        related_name="ID_Voyage"
    )

    def __str__(self) -> str:
        return self.IDLigneCommande