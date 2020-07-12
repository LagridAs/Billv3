from django.db.models import Avg, Count, Min, Sum, ExpressionWrapper, fields, F
from .models import Facture,Categorie
from jchart import Chart
from jchart.config import DataSet


class JourChart(Chart):
    chart_type = 'line'
    queryset = Facture.objects.values('date').annotate(chiffre_affaire=Sum(
        ExpressionWrapper(
            F('lignes__qte') * F('lignes__produit__prix'),
            output_field=fields.FloatField()
        )
    ))

    def get_datasets(self, **kwargs):
        return [DataSet(
            color=(20, 13, 120),
            data=list(self.queryset.values_list('chiffre_affaire', flat=True)),
            label="l'évolution du chiffre d'affaire"
        )]

    def get_labels(self, **kwargs):
        return list(self.queryset.values_list('date', flat=True))


class CategorieChart(Chart):
    chart_type = 'radar'
    queryset = Facture.objects.values('lignes__produit__categorie').annotate(chiffre_affaire=Sum(
        ExpressionWrapper(
            F('lignes__qte') * F('lignes__produit__prix'),
            output_field=fields.FloatField()
        )
    ))

    def get_datasets(self, **kwargs):
        return [DataSet(
            color=(13, 200, 56),
            data=list(self.queryset.values_list('chiffre_affaire', flat=True)),
            label="chiffre d'affaire par Categorie"
        )]

    def get_labels(self, **kwargs):
        return list(self.queryset.values_list('lignes__produit__categorie', flat=True))



