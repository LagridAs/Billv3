from turtle import onclick

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, HTML
from django.db.models import ExpressionWrapper, F, FloatField, fields, Sum
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from bill.jcharts import JourChart, CategorieChart
from bill.models import Facture, Client, LigneFacture, Fournisseur, Commande, Panier,Produit,Categorie

# Create your views here.
from bill.table import FactureTable, ClientTable, CommandeTable,PanierTable, LigneFactureTable, FournisseurTable, ChiffreFournisseurTab, \
    ChiffreClientTab,ProduitTable


def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context = {}
    context['facture'] = facture
    return render(request, 'facture_detail.html', context)


class FactureUpdate(UpdateView):
    model = Facture
    fields = ['client', 'date']
    template_name = 'update.html'

    success_message = "La facture a été mise à jour avec succès"

    def get_form(self, form_class=None):
        messages.warning(self.request, "Attention, vous allez modifier la facture")
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-warning'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(FactureUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Modifier facture'
        return context


class FactureDetailView(DetailView):
    template_name = 'facture_table_detail.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)

        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'create.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(LigneFactureCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter Ligne facture'
        return context


class LigneFactureUpdateView(UpdateView):
    model = LigneFacture
    template_name = 'update.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(LigneFactureUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Modifier ligne facture'
        return context


class LigneFactureDeleteView(DeleteView):
    model = LigneFacture
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})

    def get_context_data(self, **kwargs):
        context = super(LigneFactureDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Supprimer Ligne de facture'
        return context


class ClientList(SingleTableView):
    model = Client
    table_class = ClientTable
    template_name = 'list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all().annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('facture__lignes__qte') * F('facture__lignes__produit__prix'),
                output_field=fields.FloatField()
            )
        ))
        context['object_table'] = self.table_class(context["object_list"])
        context['title'] = "Liste des clients"
        context['option'] = "Ajouter Client"
        context['ajouter_url'] = reverse('client_create')
        context['object_name'] = "Client"
        return context


class CreateClient(CreateView):
    model = Client
    template_name = 'create.html'
    fields = ['nom', 'prenom', 'adresse', 'tel', 'sexe']

    def get_form(self, form_class=None):
        form = super(CreateClient, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Creer', css_class='btn btn-success'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('client_list'))))
        self.success_url = reverse('client_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateClient, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter client'
        return context


class EditClient(UpdateView):
    model = Client
    template_name = 'update.html'
    fields = ['nom', 'prenom', 'adresse', 'tel', 'sexe']

    def get_form(self, form_class=None):
        form = super(EditClient, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Enregister', css_class='btn btn-success'))
        form.helper.add_input(Button('Cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('client_list'))))
        self.success_url = reverse('client_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(EditClient, self).get_context_data(**kwargs)
        context['title'] = 'Modifier client'
        return context


class DeleteClient(DeleteView):
    model = Client
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('client_list')

    def get_context_data(self, **kwargs):
        context = super(DeleteClient, self).get_context_data(**kwargs)
        context['title'] = 'Supprimer Client'
        return context


class ProduitList(SingleTableView):
    model = Produit
    table_class = ProduitTable
    template_name = 'list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all()
        context['object_table'] = self.table_class(context["object_list"])
        context['title'] = "Liste des produits"
        context['option'] = "Ajouter produit"
        context['ajouter_url'] = reverse('produit_create')
        context['object_name'] = "Produit"
        return context

class CreateProduit(CreateView):
    model = Produit
    template_name = 'create.html'
    fields = ['designation','prix','fournis']

    def get_form(self, form_class=None):
        form = super(CreateProduit, self).get_form(form_class)
        form.helper = FormHelper()
        form.fields['fournis'] = forms.ModelChoiceField(queryset= Fournisseur.objects,initial=0)
        #form.fields['categorie'] = forms.ModelChoiceField(queryset=Categorie.objects, initial=0)
        form.helper.add_input(Submit('submit', 'Creer', css_class='btn btn-success'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('produit_list'))))
        self.success_url = reverse('produit_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateProduit, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter produit'
        return context

class EditProduit(UpdateView):
    model = Produit
    template_name = 'update.html'
    fields = ['designation','prix','fournis']

    def get_form(self, form_class=None):
        form = super(EditProduit, self).get_form(form_class)
        form.helper = FormHelper()
        form.fields['fournis'] = forms.ModelChoiceField(queryset= Fournisseur.objects,initial=self.kwargs.get('fournis'))
        form.helper.add_input(Submit('submit', 'Enregister', css_class='btn btn-success'))
        form.helper.add_input(Button('Cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('produit_list'))))
        self.success_url = reverse('produit_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(EditProduit, self).get_context_data(**kwargs)
        context['title'] = 'Modifier produit'
        return context


class DeleteProduit(DeleteView):
    model = Produit
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('produit_list')

    def get_context_data(self, **kwargs):
        context = super(DeleteProduit, self).get_context_data(**kwargs)
        context['title'] = 'Supprimer Produit'
        return context

class FactureList(SingleTableView):
    model = Facture
    template_name = 'list.html'
    table_class = FactureTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all().annotate(total=Sum(
            ExpressionWrapper(
                F('lignes__qte') * F('lignes__produit__prix'),
                output_field=fields.FloatField()
            )
        ))
        context['object_table'] = self.table_class(context['object_list'])
        context['title'] = 'Liste des factures'
        context['ajouter_url'] = reverse('facture_create')
        context['option'] = 'Ajouter facture'
        context['object_name'] = "Facture"
        return context

class FactureListClient(SingleTableView):
    model = Facture
    template_name = 'list.html'
    table_class = FactureTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(client_id = self.kwargs.get('pk')).annotate(total=Sum(
            ExpressionWrapper(
                F('lignes__qte') * F('lignes__produit__prix'),
                output_field=fields.FloatField()
            )
        ))
        context['object_table'] = self.table_class(context['object_list'])
        context['title'] = 'Liste des factures'
        context['ajouter_url'] = reverse('facture_create')
        context['option'] = 'Ajouter facture'
        context['object_name'] = "Facture"
        return context

 


class FactureCreate(CreateView):
    model = Facture
    template_name = 'create.html'
    fields = ['client', 'date']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.fields['date'] = forms.DateTimeField(widget=DatePickerInput(format='%m/%d/%Y'))
        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects.filter(id=self.kwargs.get('pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        print(self.kwargs.get('pk'))
        self.success_url = reverse('facture_list', kwargs={'pk': self.kwargs.get('pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(FactureCreate, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter facture'
        return context

class CreateFacture(CreateView):
    model = Facture
    template_name = 'create.html'
    fields = ['client', 'date']

    def get_form(self, form_class=None):
        form = super(CreateFacture, self).get_form(form_class)
        form.helper = FormHelper()
        form.fields['date'] = forms.DateTimeField(widget=DatePickerInput(format='%m/%d/%Y'))
        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects, initial=0)
        form.helper.add_input(Submit('submit', 'Creer', css_class='btn btn-success'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('facture_list'))))
        self.success_url = reverse('facture_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateFacture, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter facture'
        return context



class FournisseurList(SingleTableView):
    model = Fournisseur
    table_class = FournisseurTable
    template_name = 'list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all()
        context['object_table'] = self.table_class(context['object_list'])
        context['title'] = "List des Fournisseurs"
        context['option'] = "Ajouter Fournisseur"
        context['ajouter_url'] = reverse('fournisseur_create')
        context['object_name'] = "Fournisseur"
        return context


class CreateFournisseur(CreateView):
    model = Fournisseur
    template_name = 'create.html'
    fields = ['nom', 'prenom']

    def get_form(self, form_class=None):
        form = super(CreateFournisseur, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Creer', css_class='btn btn-success'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('fournisseur_list'))))
        self.success_url = reverse('fournisseur_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateFournisseur, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter fournisseur'
        return context


class EditFournisseur(UpdateView):
    model = Fournisseur
    template_name = 'update.html'
    fields = ['nom', 'prenom']

    def get_form(self, form_class=None):
        form = super(EditFournisseur, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Enregister', css_class='btn btn-success'))
        form.helper.add_input(Button('Cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('fournisseur_list'))))
        self.success_url = reverse('fournisseur_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(EditFournisseur, self).get_context_data(**kwargs)
        context['title'] = 'Modifier fournisseur'
        return context


class DeleteFournisseur(DeleteView):
    model = Fournisseur
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('fournisseur_list')

    def get_context_data(self, **kwargs):
        context = super(DeleteFournisseur, self).get_context_data(**kwargs)
        context['title'] = 'Supprimer Fournisseur'
        return context


class DashboardView(TemplateView):
    model = Facture
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['list_fournisseur'] = self.model.objects.values('lignes__produit__fournis',
                                                                'lignes__produit__fournis__nom',
                                                                'lignes__produit__fournis__prenom').annotate(
            chiffre_affaire=Sum(
                ExpressionWrapper(
                    F('lignes__qte') * F('lignes__produit__prix'),
                    output_field=fields.FloatField()
                )
            ))
        print(context['list_fournisseur'])
        context['table_fournisseur'] = ChiffreFournisseurTab(context['list_fournisseur'])
        context['list_client'] = self.model.objects.all().values('client', 'client__nom', 'client__prenom').annotate(
            chiffre_affaire=Sum(
                ExpressionWrapper(
                    F('lignes__qte') * F('lignes__produit__prix'),
                    output_field=fields.FloatField()
                )
            )).order_by('-chiffre_affaire')

        context['table_client'] = ChiffreClientTab(context['list_client'])
        print(context['list_client'])
        context['chart_jour'] = JourChart()
        context['chart_categorie'] = CategorieChart()
        return context





class CommandeDetailView(DetailView):
    template_name = 'commande_table_detail.html'
    model = Commande
    
    def get_context_data(self, **kwargs):
        context = super(CommandeDetailView, self).get_context_data(**kwargs)

        table = PanierTable(Panier.objects.filter(commande=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        #context['object'] = 'Panier'
        #context['title'] = 'Les produits de la commande : ' + str(self.get_object())

        return context



class CommandeList(SingleTableView):
    model = Commande
    template_name = 'list.html'
    table_class = CommandeTable

    def get_context_data(self, **kwargs):
        context = super(CommandeList, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all().annotate(total=Sum(
            ExpressionWrapper(
                F('paniers__qte') * F('paniers__produit__prix'),
                output_field=fields.FloatField()
            )
        ))
        context['object_table'] = self.table_class(context['object_list'])
        context['title'] = 'Liste des commandes'
        context['ajouter_url'] = reverse('commande_create')
        context['option'] = 'Ajouter commande'
        return context

class CommandeListClient(SingleTableView):
    model = Commande
    template_name = 'list.html'
    table_class = CommandeTable

    def get_context_data(self, **kwargs):
        context = super(CommandeListClient, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(client_id = self.kwargs.get('pk')).annotate(total=Sum(
            ExpressionWrapper(
                F('paniers__qte') * F('paniers__produit__prix'),
                output_field=fields.FloatField()
            )
        ))
        context['object_table'] = self.table_class(context['object_list'])
        context['title'] = 'Liste des commandes'
        context['ajouter_url'] = reverse('commande_create')
        context['option'] = 'Ajouter commande'
        return context


class CommandeCreate(CreateView):
    model = Commande
    template_name = 'create.html'
    fields = ['client']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        #form.fields['date'] = forms.DateTimeField(widget=DatePickerInput(format='%m/%d/%Y'))
        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects.filter(id=self.kwargs.get('pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        print(self.kwargs.get('pk'))
        self.success_url = reverse('commande_list', kwargs={'pk': self.kwargs.get('pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(CommandeCreate, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter commande'
        return context


class CreateCommande(CreateView):
    model = Commande
    template_name = 'create.html'
    fields = ['client']

    def get_form(self, form_class=None):
        form = super(CreateCommande, self).get_form(form_class)
        form.helper = FormHelper()
        #form.fields['date'] = forms.DateTimeField(widget=DatePickerInput(format='%m/%d/%Y'))
        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects, initial=0)
        form.helper.add_input(Submit('submit', 'Creer', css_class='btn btn-success'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-primary',
                                     onclick="window.location.href = '{}';".format(reverse('commande_list'))))
        self.success_url = reverse('commande_list')
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateCommande, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter une commande'
        return context


class PanierCreateView(CreateView):
    model = Panier
    template_name = 'create.html'
    fields = ['commande', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['commande'] = forms.ModelChoiceField(
            queryset=Commande.objects.filter(id=self.kwargs.get('commande_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('commande_table_detail', kwargs={'pk': self.kwargs.get('commande_pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(PanierCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Ajouter Panier'
        return context

class CommandeUpdate(UpdateView):
    model = Commande
    fields = ['client']
    template_name = 'update.html'

    success_message = "La commande a été mise à jour avec succès"

    def get_form(self, form_class=None):
        messages.warning(self.request, "Attention, vous allez modifier la commande")
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-warning'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('commande_table_detail', kwargs={'pk': self.kwargs.get('pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(CommandeUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Modifier commande'
        return context


class PanierUpdateView(UpdateView):
    model = Panier
    template_name = 'update.html'
    fields = ['commande', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['commande'] = forms.ModelChoiceField(
            queryset=Commande.objects.filter(id=self.kwargs.get('commande_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('commande_table_detail', kwargs={'pk': self.kwargs.get('commande_pk')})
        return form

    def get_context_data(self, **kwargs):
        context = super(PanierUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Modifier panier de commande'
        return context

class PanierDeleteView(DeleteView):
    model = Panier
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('commande_table_detail', kwargs={'pk': self.kwargs.get('commande_pk')})

    def get_context_data(self, **kwargs):
        context = super(PanierDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Supprimer Panier'
        return context
