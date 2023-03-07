from django import forms
from shop.models import Review, Tag


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', "review")


class TagsFilterForm(forms.Form):
    tag = forms.BooleanField(required=False)


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search for products"})
    )
