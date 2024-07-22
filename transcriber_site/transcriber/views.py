from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import LoginForm
import os
from transcriber_tools.transcriber import transcribation

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
@login_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_path = os.path.join('uploads', file.name)
        
       
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        
        processed_file_path = transcribation(file_path)
        
        
        download_url = f'/download/{os.path.basename(processed_file_path)}'
        return JsonResponse({'download_url': download_url})
    
    return render(request, 'index.html')

@login_required
def download_file(request, filename):
    file_path = os.path.join('processed_files', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
    else:
        return JsonResponse({'error': 'File not found'}, status=404)
