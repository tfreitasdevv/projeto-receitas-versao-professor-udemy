from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

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
        'form_action': reverse('authors:create'),
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

    return redirect('authors:register')
