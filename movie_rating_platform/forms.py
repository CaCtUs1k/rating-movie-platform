from django import forms
from django.contrib.auth.forms import UserCreationForm

from movie_rating_platform.models import Visitor, Rating


class MovieSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )


class VisitorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class VisitorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Visitor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "wishlist",
        )


class VisitorUpdateForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ("first_name", "last_name", "username", "email")


class CreateOrUpdateRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value", "description"]

        widgets = {
            "value": forms.TextInput(
                attrs={"placeholder": "Enter value from 0 to 10"}
            ),
            "description": forms.TextInput(
                attrs={"placeholder": "Enter description"}
            ),
        }

        labels = {
            "value": "",
            "description": "",
        }
