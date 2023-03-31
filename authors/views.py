from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404

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
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    # aqui se cria a chave register_form_data na session e atribui o post
    # inteiro a essa chave
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(request.POST)
    return redirect('authors:register')
