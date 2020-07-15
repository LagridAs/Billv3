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
from bill.views import ClientList, CreateClient, EditClient, DeleteClient,ProduitList,CreateProduit,EditProduit, DeleteProduit,FactureList,\
                         CommandeList,CreateFacture,CreateCommande,FactureListClient,CommandeListClient,LoginView, LogoutView



urlpatterns = [
    path('', views.home, name="home"),
    path("select2/", include("django_select2.urls")),
    path('accounts/register/', views.signup, name="signup"),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
    #re_path(r'^accounts/login/$', LoginView.as_view(), name='login'),
    #re_path(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),
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
    re_path(r'^facture_list/(?P<pk>\d+)/$', FactureListClient.as_view(), name='facture_list'),
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
    re_path(r'^commande_list/$', CommandeList.as_view(), name='commande_list'),
    re_path(r'^commande_list/(?P<pk>\d+)$', CommandeListClient.as_view(), name='commande_list'),
    #re_path(r'^commande_list_confirmees/$', CommandeListConfirme.as_view(), name='commande_list_confirmees'),
    re_path(r'^commande_create/$', CreateCommande.as_view(), name='commande_create'),
    re_path(r'^commande_table_detail/(?P<pk>\d+)/$', views.CommandeDetailView.as_view(), name='commande_table_detail'),
    re_path(r'^commande_table_create/(?P<commande_pk>\d+)/$', views.PanierCreateView.as_view(),
            name='commande_table_create'),
    re_path(r'^commande_update/(?P<pk>\d+)/$', views.CommandeUpdate.as_view(), name='commande_update'),
    re_path(r'^panier_update/(?P<pk>\d+)/(?P<commande_pk>\d+)/$', views.PanierUpdateView.as_view(),
            name='panier_update'),
    re_path(r'^panier_delete/(?P<pk>\d+)/(?P<commande_pk>\d+)/$', views.PanierDeleteView.as_view(),
            name='panier_delete'),
    re_path(r'^fournisseur_list/$', views.FournisseurList.as_view(), name='fournisseur_list'),
    re_path(r'^fournisseur_create/$', views.CreateFournisseur.as_view(), name='fournisseur_create'),
    re_path(r'^fournisseur_edit/(?P<pk>\d+)/$',views.EditFournisseur.as_view(), name='fournisseur_edit'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.DeleteFournisseur.as_view(), name='fournisseur_delete'),
    re_path(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
