
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Client, Project

def home(request):
    return render(request, 'clients/home.html')

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'clients/user_list.html', {'users': users})

@login_required
def project_list(request):
    projects = Project.objects.filter(users=request.user)
    return render(request, 'clients/project_list.html', {'projects': projects})

# Placeholder views for other functionality
@login_required
def client_create(request):
    return render(request, 'clients/client_form.html')

@login_required
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    projects = client.projects.all()
    return render(request, 'clients/client_detail.html', {'client': client, 'projects': projects})

@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/client_form.html', {'client': client})

@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/client_confirm_delete.html', {'client': client})

@login_required
def user_create(request):
    return render(request, 'clients/user_form.html')

@login_required
def user_detail(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    projects = user_obj.assigned_projects.all()
    return render(request, 'clients/user_detail.html', {'user_obj': user_obj, 'projects': projects})

@login_required
def user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    return render(request, 'clients/user_form.html', {'user_obj': user_obj})

@login_required
def user_delete(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    return render(request, 'clients/user_confirm_delete.html', {'user_obj': user_obj})

@login_required
def project_create(request, client_id=None):
    client = None
    if client_id:
        client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        user_ids = request.POST.getlist('users')
        
        if project_name and client:
            project = Project.objects.create(
                project_name=project_name,
                client=client,
                created_by=request.user
            )
            
            # Add selected users to the project
            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)
                    project.users.add(user)
                except User.DoesNotExist:
                    pass
            
            return redirect('client_detail', client_id=client.id)
    
    users = User.objects.all()
    return render(request, 'clients/project_form.html', {'client': client, 'users': users})

@login_required
def client_json(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    data = {
        'id': client.id,
        'client_name': client.client_name,
        'created_by': client.created_by.username,
        'created_at': client.created_at.isoformat(),
        'updated_at': client.updated_at.isoformat(),
        'projects': [{'id': p.id, 'project_name': p.project_name} for p in client.projects.all()]
    }
    return JsonResponse(data)

@login_required
def user_json(request, user_id):
    user = get_object_or_404(User, id=user_id)
    data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'date_joined': user.date_joined.isoformat(),
        'assigned_projects': [{'id': p.id, 'project_name': p.project_name, 'client': p.client.client_name} for p in user.assigned_projects.all()]
    }
    return JsonResponse(data)

@login_required
def project_json(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    data = {
        'id': project.id,
        'project_name': project.project_name,
        'client': {
            'id': project.client.id,
            'client_name': project.client.client_name
        },
        'created_by': {
            'id': project.created_by.id,
            'username': project.created_by.username,
            'first_name': project.created_by.first_name,
            'last_name': project.created_by.last_name
        },
        'assigned_users': [
            {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            } for user in project.users.all()
        ],
        'created_at': project.created_at.isoformat(),
        'updated_at': project.updated_at.isoformat()
    }
    return JsonResponse(data)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
