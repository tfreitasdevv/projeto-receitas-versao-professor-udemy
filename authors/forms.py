from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'password': 'Senha',
        }
        help_texts = {
            'email': 'O e-mail deve ser válido',
        }
        error_messages = {
            'username': {
                'required': 'Este campo é de preenchimento obrigatório',
                'invalid': 'O campo é inválido'
            },
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Digite aqui seu nome de usuário'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Insira sua senha'
            }),
        }
