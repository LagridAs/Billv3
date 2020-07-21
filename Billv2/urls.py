"""Billv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from Billv2 import settings
from bill import views
from bill.views import ClientList, CreateClient, EditClient, DeleteClient, ProduitList, CreateProduit, EditProduit, \
    DeleteProduit, FactureList, \
    CreateFacture, FactureListClient, LoginView, LogoutView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('accounts/register/', views.signup, name="signup"),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^client_list/$', ClientList.as_view(), name='client_list'),
    re_path(r'^client_create/$', CreateClient.as_view(), name='client_create'),
    re_path(r'^client_edit/(?P<pk>\d+)/$', EditClient.as_view(), name='client_edit'),
    re_path(r'^client_delete/(?P<pk>\d+)/$', DeleteClient.as_view(), name='client_delete'),
    re_path(r'^produit_list/$', ProduitList.as_view(), name='produit_list'),
    re_path(r'^produit_create/$', CreateProduit.as_view(), name='produit_create'),
    re_path(r'^produit_edit/(?P<pk>\d+)/$', EditProduit.as_view(), name='produit_edit'),
    re_path(r'^produit_delete/(?P<pk>\d+)/$', DeleteProduit.as_view(), name='produit_delete'),
    re_path(r'^facture_list/$', FactureList.as_view(), name='facture_list'),
    re_path(r'^facture_list_client/(?P<pk>\d+)/$', FactureListClient.as_view(), name='facture_list_client'),
    re_path(r'^facture_create/$', CreateFacture.as_view(), name='facture_create'),
    re_path(r'^facture_table_detail/(?P<pk>\d+)/$', views.FactureDetailView.as_view(), name='facture_table_detail'),
    re_path(r'^facture_table_create/(?P<facture_pk>\d+)/$', views.LigneFactureCreateView.as_view(),
            name='facture_table_create'),
    re_path(r'^lignefacture_delete/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureDeleteView.as_view(),
            name='lignefacture_delete'),
    re_path(r'^lignefacture_update/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureUpdateView.as_view(),
            name='lignefacture_update'),
    re_path(r'^facture_update/(?P<pk>\d+)/$', views.FactureUpdate.as_view(), name='facture_update'),
    re_path(r'^facture_create/(?P<pk>\d+)/$', views.FactureCreate.as_view(), name='facture_create'),
    re_path(r'^fournisseur_list/$', views.FournisseurList.as_view(), name='fournisseur_list'),
    re_path(r'^fournisseur_create/$', views.CreateFournisseur.as_view(), name='fournisseur_create'),
    re_path(r'^fournisseur_edit/(?P<pk>\d+)/$',views.EditFournisseur.as_view(), name='fournisseur_edit'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.DeleteFournisseur.as_view(), name='fournisseur_delete'),
    re_path(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    re_path(r'^addToPanier/(?P<pk>\d+)/$', views.addToPanier, name='addToPanier'),
    re_path(r'^produit_client_list/$', views.ProduitListClient.as_view(), name='produit_client_list'),
    re_path(r'^panier_detail/(?P<pk>\d+)/$', views.PanierDetailView.as_view(), name='panier_detail'),
    re_path(r'^commande_confirmation/(?P<pk>\d+)/$', views.confirmerCommande, name='commande_confirmation'),
    re_path(r'^lignecommande_delete/(?P<pk>\d+)/(?P<commande_pk>\d+)/$', views.LigneCmdDelete.as_view(),
            name='lignecmd_delete'),
    re_path(r'^lignecommande_update/(?P<pk>\d+)/(?P<commande_pk>\d+)/$', views.LigneCmdUpdate.as_view(),
            name='lignecmd_update'),
    re_path(r'^commande_listAdmin/$', views.CommandeList.as_view(),name='commande_listAdmin'),
    re_path(r'^commande_listClient_Valide/(?P<pk>\d+)$', views.CommandeListClientVal.as_view(),
            name='commande_listClient_valide'),
    re_path(r'^commande_listClient_NonValide/(?P<pk>\d+)$', views.CommandeListClientNonVal.as_view(),
            name='commande_listClient_non_valide'),

    re_path(r'^commande_details/(?P<pk>\d+)/$', views.CommandeDetailsAdmin.as_view(),name='commande_details'),
    re_path(r'^commande_validation/(?P<pk>\d+)/$', views.validerCommande,name='commande_validation'),



]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
