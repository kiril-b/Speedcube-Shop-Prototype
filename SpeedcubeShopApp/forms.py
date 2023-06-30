from django import forms
from .models import *


class PuzzleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PuzzleForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Puzzle
        exclude = ('employee_session', 'date_time_added', 'category')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name'}),
            'price': forms.TextInput(attrs={'placeholder': 'Price'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Brand'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description...', 'style': 'height: 100%'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'Quantity'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Image URL'}),
        }


class AccessoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccessoryForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Accessory
        exclude = ('employee_session', 'date_time_added', 'category')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name'}),
            'price': forms.TextInput(attrs={'placeholder': 'Price'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Brand'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description...'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'Quantity'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Image URL'}),
        }
