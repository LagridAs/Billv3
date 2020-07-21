import django_filters
from django_filters import rest_framework as filters
from bill.models import Client, Fournisseur, Produit, Commande, Facture
from django.db import models
from django_filters import DateRangeFilter, DateFilter


class ClientFilter(django_filters.FilterSet):
    user__last_name = filters.CharFilter(label='last name', lookup_expr='icontains')
    user__first_name = filters.CharFilter(label='last name', lookup_expr='icontains')
    user__profile__adresse = filters.CharFilter(label='adr', lookup_expr='icontains')
    user__profile__tel = filters.CharFilter(label='tel', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = '__all__'


class FournisseurFilter(django_filters.FilterSet):
    user__last_name = filters.CharFilter(label='last name', lookup_expr='icontains')
    user__first_name = filters.CharFilter(label='first name', lookup_expr='icontains')

    class Meta:
        model = Fournisseur
        fields = []


class ProduitFilter(django_filters.FilterSet):
    designation = filters.CharFilter(label='designation', lookup_expr='icontains')
    categorie__intitule = filters.CharFilter(label='categorie', lookup_expr='icontains')
    prix = filters.NumberFilter(label='prix', lookup_expr='iexact')
    prix__gt = django_filters.NumberFilter(field_name='prix', lookup_expr='gt',label='prix >')
    prix__lt = django_filters.NumberFilter(field_name='prix', lookup_expr='lt',label='prix <')

    class Meta:
        models = Produit
        exclude = ['photo']


class CommandeFilter(django_filters.FilterSet):
    date = DateRangeFilter(label='Date_Range')

    class Meta:
        model = Commande
        fields = ['client']


class FactureFilter(django_filters.FilterSet):
    date = DateRangeFilter(label='Date_Range')

    class Meta:
        model = Facture
        fields = ['client']


class CommandeFilterClient(django_filters.FilterSet):
    date = DateRangeFilter(label='Date_Range')

    class Meta:
        model = Commande
        fields = []


class FactureFilterClient(django_filters.FilterSet):
    date = DateRangeFilter(label='Date_Range')

    class Meta:
        model = Facture
        fields = []
