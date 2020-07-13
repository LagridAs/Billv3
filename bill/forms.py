from django.contrib.auth.forms import UserCreationForm

import bill
from django import forms

from bill import models


class SignUpForm(UserCreationForm):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    adresse = forms.CharField(widget=forms.Textarea)
    tel = forms.CharField(max_length=10)
    sexe = forms.ChoiceField(choices=SEXE)

    class Meta(UserCreationForm.Meta):
        model = models.UserInstallment
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','roles','adresse','tel','sexe']
