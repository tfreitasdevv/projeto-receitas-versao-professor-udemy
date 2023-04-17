from django import forms
from recipes.models import Recipe


class RecipeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
