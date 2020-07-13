from django.contrib.auth.models import AbstractUser
from django.db import models
from django import utils

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Role(models.Model):
    ADMIN = 1
    Fournisseur = 2
    Client = 3

    ROLE_CHOICES = (
        (Client, 'client'),
        (Fournisseur, 'fournisseur'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class UserInstallment(AbstractUser):
    roles = models.ManyToManyField(Role)


class Profile(models.Model):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    user = models.OneToOneField(UserInstallment, on_delete=models.CASCADE, related_name="profile", null=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE)

    @receiver(post_save, sender=UserInstallment)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            print("dakhal if created")
            print(instance)
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return str(self.user)


class Client(models.Model):
    user = models.OneToOneField(UserInstallment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Fournisseur(models.Model):
    user = models.OneToOneField(UserInstallment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return  self.user.username


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
