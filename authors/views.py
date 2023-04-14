from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm

# Create your views here.


def register_view(request):
    # o session armazena informações em cookies no navegador do usuário.
    # O number foi criado, qualquer valor pode ser criado aqui.
    request.session['number'] = request.session.get('number') or 1
    request.session['number'] += 1

    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    # aqui se cria a chave register_form_data na session e atribui o post
    # inteiro a essa chave
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        # o commit false faz com que os dados não sejam salvos imediatamente
        # na base de dados, mas fiquem armazenados
        user = form.save(commit=False)
        # isso faz com que o password seja salvo criptografado
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Seu usuário foi criado, faça o login')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Login feito com sucesso.')
            login(request, authenticated_user)
            return redirect(reverse('authors:dashboard'))

        messages.error(request, 'Credenciais inválidas')
        return redirect(login_url)

    messages.error(request, 'Erro ao validar dados do formulário')
    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):

    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )

    return render(request, 'authors/pages/dashboard.html', {
        'recipes': recipes,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):

    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/pages/dashboard_recipe.html', {
        'form': form
    })
