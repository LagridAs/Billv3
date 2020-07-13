from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from bill.models import Client, Produit, Facture, LigneFacture, Fournisseur, UserInstallment, Role

# Register your models here.
admin.site.register(Client)
admin.site.register(Facture)
admin.site.register(Produit)
admin.site.register(LigneFacture)
admin.site.register(Fournisseur)
admin.site.register(UserInstallment, UserAdmin)
admin.site.register(Role)
