
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'first_name', 'last_name', 'email']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_at', 'created_by', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    name = serializers.CharField(source='project_name', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'project_name', 'client_name', 'users', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']

class ClientDetailSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_at', 'created_by', 'updated_at']
    
    def get_projects(self, obj):
        projects = obj.projects.all()
        return [{'id': p.id, 'name': p.project_name} for p in projects]

class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.ListField(child=serializers.DictField(), write_only=True)
    client = serializers.CharField(source='client.client_name', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']
    
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        
        # Add users to project
        for user_data in users_data:
            try:
                user = User.objects.get(id=user_data['id'])
                project.users.add(user)
            except User.DoesNotExist:
                pass
        
        return project
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'project_name': instance.project_name,
            'client': instance.client.client_name,
            'users': [{'id': user.id, 'name': user.username} for user in instance.users.all()],
            'created_at': instance.created_at,
            'created_by': instance.created_by.username
        }
