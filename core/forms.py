# -*- coding:utf-8 -*-

from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from core.models import Product

class SearchForm(forms.Form):
    words=forms.TextField()
    
class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('updated','created',)

        