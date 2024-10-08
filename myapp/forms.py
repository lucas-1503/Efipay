from django import forms
from .models import Charge

class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ['customer','value', 'description']