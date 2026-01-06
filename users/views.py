from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import *


def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect Username Password')
    context = {'form': forms}
    return render(request, 'users/login.html', context)



def resgister_user(request):

    forms = registerForm()
    if request.method == 'POST':
        forms = registerForm(request.POST)
        if forms.is_valid():
            forms_instance = forms.save(commit = False)
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                
                messages.error(request, 'user already exsist')
                return redirect('list_user')
            else:
                
                forms_instance.password_r = password
                forms_instance.save()

                return redirect('list_user')
        else:
            context = {'form': forms}

            return render(request, 'users/resgister.html', context)
    else:
        context = {'form': forms}

        return render(request, 'users/resgister.html', context)


def update_user(request, user_id):

    instance = User.objects.get(id = user_id)

    password = request.POST.get('password1')
    

    if not password:

        password = instance.password_r


    forms = registerForm(instance = instance)
    if request.method == 'POST':

        updated_request = request.POST.copy()
        updated_request.update({'password1': password})
        forms = registerForm(updated_request, instance = instance)
        if forms.is_valid():
            forms_instance = forms.save(commit = False)
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password1']
            user = authenticate(username=username)
            if user:

                messages.error(request, 'user already exsist')
                return redirect('list_use   r')
            else:

                forms_instance.password_r = password
                forms_instance.save()

                return redirect('list_user')
        else:
            context = {'form': forms}

            return render(request, 'users/update_user.html', context)

    else:
        context = {'form': forms}

        return render(request, 'users/update_user.html', context)


def delete_user(request, user_id):

    User.objects.get(id = user_id).delete()
    
    return redirect('list_user')

def list_user(request):

    data = User.objects.all().order_by('-id')
    
    return render(request, 'users/list_user.html', {'data' : data})

def logout_page(request):
    logout(request)
    return redirect('login')
