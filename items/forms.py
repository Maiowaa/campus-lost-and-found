from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Claim, CATEGORY_CHOICES, ITEM_TYPE_CHOICES


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.help_text = ''


class ItemForm(forms.ModelForm):
    date_item = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        label='Date lost/found'
    )

    class Meta:
        model = Item
        fields = [
            'title', 'description', 'item_type',
            'category', 'location', 'date_item', 'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Black Leather Wallet',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the item in detail...',
            }),
            'item_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Main Library, 2nd Floor',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe why you believe this item is yours...',
            }),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, description, location...',
        }),
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + list(CATEGORY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    item_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(ITEM_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
