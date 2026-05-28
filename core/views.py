from django.shortcuts import render

# Create your views here.
from entities.models import Agent
from .models import Commission
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):

    agent = Agent.objects.filter(user=request.user).first()

    commissions = None
    if agent:
        commissions = Commission.objects.filter(agent=agent).first()

    context = {
        'layout_style': 'layouts/dashboard_layout.html',
        'commissions': commissions
    }

    return render(request, 'core/dashboard.html', context)