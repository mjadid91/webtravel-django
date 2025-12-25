from django.db import models

class Ville(models.Model):
    IDVille = models.AutoField(primary_key=True)
    NomVille = models.CharField(max_length=50)
    NomPays = models.CharField(max_length=50)

    def __str__(self) -> str :
        return self.NomVille + " (" + self.NomPays + ")"


class Voyage(models.Model):
    IDVoyage = models.AutoField(primary_key=True)
    Titre = models.CharField(max_length=50)
    Prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(default='imagesUsers/default.jpg', upload_to='images')

    def __str__(self) -> str :
        return f"{self.Titre} pour {str(self.Prix)} €"


class Etape(models.Model):
    class Meta:
        unique_together = ('voyage', 'ville')

    IDEtape = models.AutoField(primary_key=True)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)

    Nb_jours = models.CharField(max_length=50)

    def __str__(self) -> str :
        vil = self.ville
        voy = self.voyage
        return vil.NomVille + ' est une étape de ' + voy.Titre + ' (' + self.Nb_jours + ' jour)'
        
