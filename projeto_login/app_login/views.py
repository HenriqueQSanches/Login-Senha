from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import re
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'pages/index.html')
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
def login(request):
    senha_error = None
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # Adicione debugging aqui
        print(f"Attempting to authenticate user with email: {email}")

        user = authenticate(request, username=email, password=password)
        
        # Adicione debugging aqui
        print(f"Authentication result: {user}")

        if user is not None:
            auth_login(request, user)
            return redirect('gerenciar')
        else:
            senha_error = "Senha ou e-mail não estão corretos ou não estão cadastrados!"
            password = ''
    return render(request, 'pages/login.html', {'senha_error': senha_error})
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
@login_required
def gerenciar(request):
    user = User.get_email_field_name
    user_first_name = request.user.first_name
    context = {
        'user_email': user,
        'user_first_name': user_first_name,
    }
    return render(request, 'pages/todo.html', context)
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
@login_required
def atualizar_cadastro(request):
    email_error = None
    
    if request.method == "POST":
        email = request.POST.get('email')
        user_email = request.user.username
        
        if email != user_email:
            email_error = "Insira um e-mail existente em que você está logado!"
        else:
            return render(request, 'pages/atualizarUser.html') 

    return render(request, 'pages/atualizar.html', {'email_error': email_error})
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
@login_required
def atualizarUser(request):
    email_error = None
    password_error = None

    if request.method == 'POST':
        email = request.POST.get('email').strip()
        user_email = request.user.username.strip()
        new_name = request.POST.get('new_name').strip()
        new_email = request.POST.get('new_email').strip()
        new_password = request.POST.get('new_password').strip()

        print(f"Email fornecido: {email}")
        print(f"Email autenticado: {user_email}")

        if email != user_email:
            email_error = 'O email fornecido não corresponde ao email autenticado.'
            return render(request, 'pages/atualizarUser.html', {
                'email_error': email_error
            })

        if new_email and new_email != user_email and User.objects.filter(username=new_email).exists():
            email_error = 'Esse e-mail já está em uso.'
            return render(request, 'pages/atualizarUser.html', {
                'email_error': email_error
            })

        if new_password and not senha_valida(new_password):
            password_error = 'A senha deve ter pelo menos 8 caracteres, incluir uma letra maiúscula, um numeral e um símbolo.'
            return render(request, 'pages/atualizarUser.html', {
                'password_error': password_error
            })

        user = request.user
        user.first_name = new_name
        if new_email and new_email != user_email:
            user.username = new_email 
        if new_password:
            user.set_password(new_password)
        user.save()

        messages.success(request, 'Seus dados foram atualizados com sucesso! Por favor, faça login novamente com suas novas credenciais.')
        return redirect('login')

    return render(request, 'pages/atualizarUser.html', {
        'email_error': email_error,
        'password_error': password_error
    })
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
def senha_valida(senha):
    if len(senha) < 8:
        return False
    if not re.search(r'[A-Z]', senha): 
        return False
    if not re.search(r'[0-9]', senha): 
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha): 
        return False
    return True
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
def cadastro(request):
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirma_senha = request.POST['confirma_senha']

        email_error = None
        senha_error = None

        if senha != confirma_senha:
            senha_error = "As senhas não coincidem."
            senha = ""
            confirma_senha = ""
        elif User.objects.filter(username=email).exists():  
            email_error = "Este email já está registrado."
            email = ""
            senha = ""
            confirma_senha = ""
        elif not senha_valida(senha):
            senha_error = "A senha deve ter pelo menos 8 caracteres, incluir uma letra maiúscula, um numeral e um símbolo."
        else:
            # Crie o novo usuário
            User.objects.create_user(username=email, password=senha, first_name=nome, is_active=True)
            return redirect('login') 

        return render(request, 'pages/cadastro.html', {
            'nome': nome,
            'email': email,
            'senha': senha,
            'email_error': email_error,
            'senha_error': senha_error
        })

    return render(request, 'pages/cadastro.html')
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
@login_required
def deletar(request):
    email_error = None
    
    if request.method == "POST":
        email = request.POST.get('email').strip()
        user_email = request.user.username.strip()

        if email != user_email:
            email_error = "Insira um e-mail existente em que VOCÊ está logado!"
        else:

            user = request.user
            user.delete()

            messages.success(request, 'Seu cadastro foi excluído com sucesso!')
            return redirect('index')  

    return render(request, 'pages/deletar.html', {'email_error': email_error})
# --------------------------------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------------------------------- #
def logout(request):
    auth_logout(request)
    return redirect('login')
# --------------------------------------------------------------------------------------------------------------------------------------------- #