from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TravelUser(User):
    # fichier image de l'user
    image = models.ImageField(default='imagesUsers/default.jpg', upload_to='imagesUsers')