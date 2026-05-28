from django.shortcuts import render,redirect

# Create your views here.
from django.http import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout                                                 
from django.contrib import auth, messages
from .forms import LoginForm
from django.urls import reverse
from entities.models import Agent
from core.models import Commission

def user_logout(request):
    logout(request)
    return redirect("/")



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

            if user is not None:
                if user.is_active:

                    agent_exists = Agent.objects.filter(
                        user=user,
                        agent_cid=int(cd['agent_id'])
                    ).exists()

                    if agent_exists:
                        login(request, user)
                        return redirect("home")
                    else:
                        return HttpResponse("Invalid Agent ID")

                else:
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('Invalid login')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})



def staff_user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

            if user is not None:
            
                login(request, user)
                return redirect("home")
                else:
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('Invalid login')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})



    