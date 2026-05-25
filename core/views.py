from django.shortcuts import render

# Create your views here.

def dashboard(request):
	context = {
        # 'layout_style': 'layouts/auth_layout.html'
        'layout_style': 'layouts/dashboard_layout.html'
    }
	return render(request, 'core/dashboard.html', context)