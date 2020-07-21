import django_tables2 as tables

from bill.models import Client, Facture, LigneFacture, Fournisseur, Commande, Produit, LigneCommande


class ClientTable(tables.Table):
    T1 = '<span> </span> <a href="{% url "client_delete" record.id %}" class="btn btn-danger">Delete</a>' \
         '<span> </span> <a href="{% url "facture_list_client" record.id %}" class="btn btn-info">Facture</a>'
    edit = tables.TemplateColumn(T1)

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "user__last_name", "user__first_name", "user__email", "user__profile__tel",
                  "user__profile__sexe", "chiffre_affaire")


class FactureTable(tables.Table):
    T1 = '<a href="{% url "facture_table_detail" record.id %}" class="btn btn-primary">Details</a>'
    details = tables.TemplateColumn(T1)

    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap.html"
        fields = ("id","client","date", "total")


class LigneFactureTable(tables.Table):
    action = '<a href="{% url "lignefacture_update" pk=record.id facture_pk=record.facture.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "lignefacture_delete" pk=record.id facture_pk=record.facture.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__id', 'produit__prix', 'qte')


class LigneCommandeTable(tables.Table):
    action = '<a href="{% url "lignecmd_update" pk=record.id commande_pk=record.commande.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "lignecmd_delete" pk=record.id commande_pk=record.commande.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = LigneCommande
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
    T2 = '<img src="../media/{{record.photo}}" width="150px" height="100px" />'
    photo = tables.TemplateColumn(T2)
    T1 = '<p>{{record.prix}}</p>'
    prix = tables.TemplateColumn(T1)

    T3 = '<a href="{% url "produit_edit" record.id %}" class="btn btn-success">Modifier</a>' \
         '<span> </span> <a href="{% url "produit_delete" record.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(T3)

    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "designation", "prix")


class ChiffreFournisseurTab(tables.Table):
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap.html"
        fields = ("lignes__produit__fournis", "lignes__produit__fournis__user__last_name",
                  "lignes__produit__fournis__user__first_name", "chiffre_affaire")


class ChiffreClientTab(tables.Table):
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap.html"
        fields = ("client", "client__user__last_name", "client__user__first_name", "chiffre_affaire")


class ProduitClientTable(tables.Table):
    T2 = '<img src="../media/{{record.photo}}" width="150px" height="100px" />'
    photo = tables.TemplateColumn(T2)
    T1 = '<a href="{% url "addToPanier" record.id %}" class="btn btn-success" id="ajouter">Ajouter au Panier</a>'
    edit = tables.TemplateColumn(T1)
    categorie__intitule = tables.Column(verbose_name= 'Categorie' )


    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap.html"
        fields = ["designation", "prix","categorie__intitule"]


class LigneCommandeTableAdmin(tables.Table):
    class Meta:
        model = LigneCommande
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__id', 'produit__prix', 'qte')


# chiffre d'affaire a ajouté
class CommandeTable(tables.Table):
    T1 = '<a href="{% url "commande_details" record.id %}" class="btn btn-success">Details</a>'
    edit = tables.TemplateColumn(T1)

    class Meta:
        model = Commande
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "client__user__username", "date")
