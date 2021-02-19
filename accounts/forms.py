from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    instituicao = forms.ChoiceField(
        choices=User.TIPO_INSTITUICAO,
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "instituicao",)
