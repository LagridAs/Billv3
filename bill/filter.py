import django_filters
from django_filters import rest_framework as filters
from bill.models import Client, Fournisseur


class ClientFilter(django_filters.FilterSet):
    user__last_name = filters.CharFilter(label='last name',lookup_expr='icontains')
    user__first_name = filters.CharFilter(label='last name',lookup_expr='icontains')
    user__profile__adresse = filters.CharFilter(label='adr',lookup_expr='icontains')
    user__profile__tel = filters.CharFilter(label='tel',lookup_expr='icontains')

    class Meta:
        model = Client
        fields = '__all__'


class FournisseurFilter(django_filters.FilterSet):
    user__last_name = filters.CharFilter(label='last name',lookup_expr='icontains')
    user__first_name = filters.CharFilter(label='first name',lookup_expr='icontains')

    class Meta:
        model = Fournisseur
        fields = []

