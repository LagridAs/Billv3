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
from bill.views import ClientList, CreateClient, EditClient, DeleteClient, FactureList


urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.signup, name="signup"),
    path('admin/', admin.site.urls),
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^client_list/$', ClientList.as_view(), name='client_list'),
    re_path(r'^client_create/$', CreateClient.as_view(), name='client_create'),
    re_path(r'^client_edit/(?P<pk>\d+)/$', EditClient.as_view(), name='client_edit'),
    re_path(r'^client_delete/(?P<pk>\d+)/$', DeleteClient.as_view(), name='client_delete'),
    re_path(r'^facture_list/(?P<pk>\d+)/$', FactureList.as_view(), name='facture_list'),
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
]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
