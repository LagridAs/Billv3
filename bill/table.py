import django_tables2 as tables

from bill.models import Client, Facture, LigneFacture, Fournisseur, Commande, Panier,Produit


class ClientTable(tables.Table):
    T1 = '<span> </span> <a href="{% url "client_delete" record.id %}" class="btn btn-danger">Delete</a>' \
         '<span> </span> <a href="{% url "facture_list" pk=record.id %}" class="btn btn-info">Facture</a>'
    edit = tables.TemplateColumn(T1)

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "user__last_name", "user__first_name", "user__profile__adresse", "user__profile__tel", "user__profile__sexe", "chiffre_affaire")


class FactureTable(tables.Table):
    T1 = '<a href="{% url "facture_table_detail" record.id %}" class="btn btn-primary">Details</a>'
    details = tables.TemplateColumn(T1)

    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "date", "total")


class LigneFactureTable(tables.Table):
    action = '<a href="{% url "lignefacture_update" pk=record.id facture_pk=record.facture.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "lignefacture_delete" pk=record.id facture_pk=record.facture.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__id', 'produit__prix', 'qte')


class FournisseurTable(tables.Table):
    T1 = '<span> </span> <a href="{% url "fournisseur_delete" record.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(T1)

    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "user__last_name", "user__first_name")


class ProduitTable(tables.Table):
    T1 = '<a href="{% url "produit_edit" record.id %}" class="btn btn-success">Modifier</a>' \
         '<span> </span> <a href="{% url "produit_delete" record.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(T1)

    class Meta : 
        model = Produit
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "designation", "prix","fournis")

    
class ChiffreFournisseurTab(tables.Table):
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap.html"
        fields = ("lignes__produit__fournis","lignes__produit__fournis__user__last_name",
                "lignes__produit__fournis__user__first_name","chiffre_affaire")


class ChiffreClientTab(tables.Table):
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap.html"
        fields = ("client","client__user__last_name","client__user__first_name", "chiffre_affaire")


class CommandeTable(tables.Table):
    T1 = '<a href="{% url "commande_table_detail" record.id %}" class="btn btn-primary">Details</a>' \
            '<span> </span> <a href="{% url "commande_table_detail" record.id %}" class="btn btn-warning">Valider</a>'
    details = tables.TemplateColumn(T1)
    

    class Meta:
        model = Commande
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "date")


class PanierTable(tables.Table):
    action = '<a href="{% url "panier_update" pk=record.id commande_pk=record.commande.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "panier_delete" pk=record.id commande_pk=record.commande.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = Panier
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__id', 'produit__prix', 'qte')

