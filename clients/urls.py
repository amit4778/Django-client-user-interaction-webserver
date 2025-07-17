
from django.urls import path
from . import views

urlpatterns = [
    # Existing URLs would be here...
    path('', views.home, name='home'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:client_id>/delete/', views.client_delete, name='client_delete'),
    
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/create/<int:client_id>/', views.project_create, name='project_create'),
    
    # JSON endpoints
    path('json/clients/<int:client_id>/', views.client_json, name='client_json'),
    path('json/users/<int:user_id>/', views.user_json, name='user_json'),
    path('json/projects/<int:project_id>/', views.project_json, name='project_json'),
    
    # Logout
    path('logout/', views.logout_view, name='logout'),
]
