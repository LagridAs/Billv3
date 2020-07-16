from turtle import onclick

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, HTML
from django.contrib.auth import authenticate, login, logout
from django.db.models import ExpressionWrapper, F, FloatField, fields, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin
from django_tables2.config import RequestConfig
from django import forms
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin

from bill.filter import ClientFilter, FournisseurFilter
from bill.forms import SignUpForm
from bill.jcharts import JourChart, CategorieChart

from bill.models import Facture, Client, LigneFacture, Fournisseur, Commande, Produit, Categorie, Role, LigneCommande
from django import utils


# Create your views here.
from bill.table import FactureTable, ClientTable, LigneFactureTable, FournisseurTable, \
    ChiffreFournisseurTab, \
    ChiffreClientTab, ProduitTable, ProduitClientTable, LigneCommandeTable, CommandeTable, LigneCommandeTableAdmin


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


class ClientList(SingleTableMixin, FilterView):
    model = Client
    table_class = ClientTable
    template_name = 'list.html'
    filterset_class = ClientFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_filtred = ClientFilter(self.request.GET, queryset=self.model.objects.all())
        data_filtredQs = data_filtred.qs
        context["object_list"] = data_filtredQs.annotate(chiffre_affaire=Sum(
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
    fields = ['user']

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
    fields = ['designation','prix','fournis','photo']

    def get_form(self, form_class=None):
        form = super(CreateProduit, self).get_form(form_class)
        form.helper = FormHelper()
        form.fields['fournis'] = forms.ModelChoiceField(queryset=Fournisseur.objects, initial=0)
        # form.fields['categorie'] = forms.ModelChoiceField(queryset=Categorie.objects, initial=0)
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
    fields = ['designation','prix','fournis','photo']

    def get_form(self, form_class=None):
        form = super(EditProduit, self).get_form(form_class)
        form.helper = FormHelper()
        form.fields['fournis'] = forms.ModelChoiceField(queryset=Fournisseur.objects,
                                                        initial=self.kwargs.get('fournis'))
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
        context['object_list'] = self.model.objects.filter(client_id=self.kwargs.get('pk')).annotate(total=Sum(
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


class FournisseurList(SingleTableMixin, FilterView):
    model = Fournisseur
    table_class = FournisseurTable
    template_name = 'list.html'
    filterset_class = FournisseurFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_filtred = FournisseurFilter(self.request.GET, queryset=self.model.objects.all())
        data_filtredQs = data_filtred.qs
        context['object_list'] = data_filtredQs
        context['object_table'] = self.table_class(context['object_list'])
        context['title'] = "List des Fournisseurs"
        context['option'] = "Ajouter Fournisseur"
        context['ajouter_url'] = reverse('fournisseur_create')
        context['object_name'] = "Fournisseur"
        return context


class CreateFournisseur(CreateView):
    model = Fournisseur
    template_name = 'create.html'
    fields = ['user']

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
                                                                'lignes__produit__fournis__user__last_name',
                                                                'lignes__produit__fournis__user__first_name').annotate(
            chiffre_affaire=Sum(
                ExpressionWrapper(
                    F('lignes__qte') * F('lignes__produit__prix'),
                    output_field=fields.FloatField()
                )
            ))
        print(context['list_fournisseur'])
        context['table_fournisseur'] = ChiffreFournisseurTab(context['list_fournisseur'])
        context['list_client'] = self.model.objects.all().values('client', 'client__user__last_name',
                                                                 'client__user__first_name').annotate(
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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("dakhal post")
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.adresse = form.cleaned_data.get('adresse')
            user.profile.tel = form.cleaned_data.get('tel')
            user.profile.sexe = form.cleaned_data.get('sexe')
            user.save()
            roleChoisis = form.cleaned_data.get('roles')
            role = roleChoisis.values_list('id', flat=True)
            print("role : ")
            list_role = list(role)
            # user.save_m2m()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            for item in list_role:
                if item == 1:
                    print("dakhal admin")
                    my_group = Group.objects.get(name='Admin')
                    print("my_group: " + str(my_group))
                    my_group.user_set.add(user)

                elif item == 2:
                    print("dakhal if fournisseur")
                    Fournisseur.objects.create(user=user)
                    my_group = Group.objects.get(name='Fournisseur')
                    print("my_group: " + str(my_group))
                    my_group.user_set.add(user)

                elif item == 3:
                    print("dakhal if Client")
                    Client.objects.create(user=user)
                    my_group = Group.objects.get(name='Client')
                    print("my_group: " + str(my_group))
                    my_group.user_set.add(user)

            return redirect('produit_list')
        else:
            print("dakhal error")
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('produit_list')

        return render(request, self.template_name)


class LogoutView(TemplateView):
    template_name = 'registration/logout.html'

    def get_success_url(self):
        return reverse('logout')

    def get(self, request, **kwargs):
        logout(request)

        return render(request, self.template_name)


def addToPanier(request, pk):
    prod = Produit.objects.filter(id=pk)
    prod = prod.first()
    quantity = 1
    user = request.user
    cmd_user = Commande.objects.filter(client__user_id=user.id, validee=False)
    if not cmd_user:
        cmdif = Commande.objects.create(client=Client.objects.get(user=request.user), panier=True, validee=False)
        ligne = LigneCommande.objects.create(produit=Produit.objects.get(id=prod.id), qte=quantity, commande=cmdif)
    else:
        cmdelse = cmd_user.first()
        ligne = LigneCommande.objects.create(produit=Produit.objects.get(id=prod.id), qte=quantity, commande=cmdelse)
    return redirect(request.META['HTTP_REFERER'])


class ProduitListClient(SingleTableView):
    model = Produit
    template_name = 'listproduit.html'
    table_class = ProduitClientTable

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all()
        context['object_table'] = self.table_class(context["object_list"])
        context['title'] = "Liste des produits"
        context['option'] = "Visualiser Panier"
        cmd_user = Commande.objects.filter(client__user_id=self.request.user, validee=False)
        if not cmd_user:
            context['confirmer_url'] = reverse('home')
        else:
            cmd = cmd_user.first().id
            context['confirmer_url'] = reverse('panier_detail', kwargs={'pk': cmd})
        context['object_name'] = "Produit"
        return context


class PanierDetailView(DetailView):
    model = Commande
    template_name = "commande_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PanierDetailView, self).get_context_data(**kwargs)

        table = LigneCommandeTable(LigneCommande.objects.filter(commande=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        context['option'] = "Confirmer Commande"
        cmd_user = Commande.objects.filter(client__user_id=self.request.user, validee=False)
        cmd = cmd_user.first().id
        context['confirmer_url'] = reverse('commande_confirmation', kwargs={'pk': cmd})
        return context


def confirmerCommande(request, pk):
    Commande.objects.filter(id=pk).update(panier=False)
    return redirect('produit_client_list')


class LigneCmdUpdate(UpdateView):
    model = LigneCommande
    template_name = 'update.html'

    fields = ['commande', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['commande'] = forms.ModelChoiceField(
            queryset=Commande.objects.filter(id=self.kwargs.get('commande_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('commande_detail', kwargs={'pk': self.kwargs.get('commande_pk')})

        return form


class LigneCmdDelete(DeleteView):
    model = LigneCommande
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('commande_detail', kwargs={'pk': self.kwargs.get('commande_pk')})

    def get_context_data(self, **kwargs):
        context = super(LigneCmdDelete, self).get_context_data(**kwargs)
        context['title'] = 'Supprimer le produit du panier'
        return context


# pour les clients et les admis ajouter un if else et 2 temp et la table

class CommandeList(SingleTableView):
    model = Commande
    template_name = 'list.html'
    table_class = CommandeTable

    def get_context_data(self, **kwargs):
        context = super(CommandeList, self).get_context_data()
        context['object_list'] = self.model.objects.filter(panier=False, validee=False)
        context['object_table'] = self.table_class(context['object_list'])
        context['title'] = 'Liste des commandes non facturées'
        context['object_name'] = 'Commandes'
        return context


class CommandeDetailsAdmin(DetailView):
    model = Commande
    template_name = "commande_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CommandeDetailsAdmin, self).get_context_data(**kwargs)

        table = LigneCommandeTableAdmin(LigneCommande.objects.filter(commande=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        context['option'] = "Valider Commande"
        context['confirmer_url'] = reverse('commande_validation', kwargs={'pk': self.kwargs.get('pk')})
        return context


def validerCommande(request, pk):
    # valide la commande
    Commande.objects.filter(id=pk).update(validee=True)
    #creation d'une facture
    commande = Commande.objects.get(id=pk)
    facture = Facture.objects.create(client=Client.objects.get(id=commande.client.id),commande=commande)
    for item in commande.lignesCmd.all():
        LigneFacture.objects.create(produit=item.produit,qte=item.qte,facture=facture)
    return redirect('commande_list')

class HomeView(TemplateView):
    template_name = 'home.html'
    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)

