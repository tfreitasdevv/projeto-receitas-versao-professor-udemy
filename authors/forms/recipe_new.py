from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError


class RecipeNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)
        # self._my_errors['bla'].append('legal')

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = (
            'title', 'description', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps', 'cover', 'category',
        )
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Fatias', 'Fatias'),
                    ('Pessoas', 'Pessoas'),
                    ('Porções', 'Porções'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                    ('Dias', 'Dias'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if len(title) < 3:
            self._my_errors['title'].append(
                'Título deve ter pelo menos 4 caracteres')

        if title == description:
            self._my_errors['title'].append(
                'Título deve ser diferente da Descrição')
            self._my_errors['description'].append(
                'Descrição deve ser diferente do Título')

        # incluir aqui as outras validações

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                'Deve ser um número positivo')

        return preparation_time
