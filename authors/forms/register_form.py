from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, new_attr_value):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {new_attr_value}'.strip()


def add_placeholder(field, placeholder_value):
    field.widget.attrs['placeholder'] = placeholder_value

# 3a forma de validação


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter letras maiúsculas, minúsculas e números,'
            'com pelo menos 8 caracteres'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'],
                 'placeholder', 'Placeholder do usuário')
        add_placeholder(self.fields['email'], 'Ph do email add placeholder')
        add_placeholder(self.fields['first_name'], 'Ex.: João')
        add_placeholder(self.fields['last_name'], 'Ex.: Silva')

    username = forms.CharField(
        label='Nome de usuário',
        help_text='Deve conter entre 4 e 150 caracteres',
        error_messages={
            'required': 'Campo obrigatório',
            'min_length': 'Campo deve ter no mínimo 4 caracteres',
            'max_length': 'Campo deve ter no máximo 150 caracteres',
        },
        min_length=4,
        max_length=150
    )

    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu primeiro nome'},
        required=True,
        label='Primeiro Nome',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        required=True,
        label='Sobrenome',
    )

    email = forms.EmailField(
        error_messages={'required': 'O e-mail é obrigatório'},
        required=True,
        label='E-mail',
        help_text='O e-mail deve ser válido',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Crie sua senha'
        }),
        error_messages={
            'required': 'Este campo é obrigatório'
        },
        label='Senha',
        validators=[strong_password]
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
            # 'username': forms.TextInput(attrs={
            #     'placeholder': 'Digite aqui seu nome de usuário'
            # }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Insira sua senha'
            }),
        }

    # exemplo de validação de um único campo.
    # o método deve ser sempre clean_nomedocampo
    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'bobo' in data:
            raise ValidationError(
                'Não digite "bobo" no campo Senha',
                code='invalid',
            )

        return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'E-mail já cadastrado na base de dados', code='invalid',
            )

        return email

    # o método clean permite fazer validações no formulário completo
    # inclusive verificando campos entre si
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': 'As senhas devem ser iguais',
                # 'password': 'As senhas devem ser iguais',
            })
