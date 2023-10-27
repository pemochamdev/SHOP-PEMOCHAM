from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('p','Paypal'),
    ('s','Stripe'),
)

class CheckoutForm(forms.Form):
    streep_address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder':'1234 Main St',
            'class':"form-control"
        })
    )
    appartment_address = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder':'Apartment or suite',
            'class':"form-control"
        })
    )
    country = CountryField(
        blank_label = '(Select country)'
    ).formfield(widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    zip  = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder':'Zip',
            'class':"form-control"
        })
    )
    same_shipping_address = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class':"custom-control-input"
        }),
        required=False
    )
    save_info = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class':"custom-control-input"
        }),
        required=False
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={
            'class':"custom-control-input"
        }), 
        choices=PAYMENT_CHOICES
    )
    