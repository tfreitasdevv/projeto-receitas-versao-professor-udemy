from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, new_attr_value):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {new_attr_value}'.strip()


def add_placeholder(field, placeholder_value):
    field.widget.attrs['placeholder'] = placeholder_value


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'],
                 'placeholder', 'Placeholder do usuário')
        add_placeholder(self.fields['email'], 'Ph do email add placeholder')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Crie sua senha'
        }),
        error_messages={
            'required': 'Este campo é obrigatório'
        },
        label='Senha',
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita a senha'
        }),
        label='Confirmação de senha'
    )

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
