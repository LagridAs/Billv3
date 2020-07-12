from django.db import models
from django import utils

# Create your models here.
from django.db.models import ExpressionWrapper, FloatField, F
from django.urls import reverse


class Client(models.Model):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(max_length=70,null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE)

    def __str__(self):
        return self.nom + ' ' + self.prenom


class Fournisseur(models.Model):
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nom + ' ' + self.prenom


class Categorie(models.Model):
    intitule = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.intitule)


class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    fournis = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.designation


class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(default=utils.timezone.now)

    def get_absolute_url(self):
        return reverse('facture_detail', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.client) + ' : ' + str(self.date)


class LigneFacture(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField(default=1)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produit', 'facture'], name="produit-facture")
        ]

