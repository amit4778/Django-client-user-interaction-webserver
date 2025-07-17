Client Management System

A Django-based web application for managing clients, projects, and user assignments. This system allows organizations to track clients, create projects for each client, and assign users to specific projects.

Features

Client Management: Create, view, edit, and delete clients

Project Management: Create projects under specific clients and assign users

User Management: View and manage system users

Project Assignment: Assign multiple users to projects

JSON API: REST API endpoints for clients, users, and projects

Interactive UI: Modern web interface with JSON data viewer

Authentication: Secure login system with Django admin integration

Tech Stack:

Backend: Django 4.2

Database: SQLite

Frontend: HTML, CSS, JavaScript

API: Django REST Framework

Authentication: Django's built-in authentication system


Project Structure:

clients/

    migrations/

        models.py

        views.py

        urls.py

        admin.py

templates/

    clients/
        client_confirm_delete.html
        client_detail.html
        client_form.html
        client_list.html
        home.html
        logout.html
        project_form.html
        project_list.html
        user_confirm_delete.html
        user_detail.html
        user_form.html
        user_list.html

    base.html

static/

    test2_main/

manage.py
Models

Client:

client_name: Name of the client
created_by: User who created the client
created_at: Creation timestamp
updated_at: Last update timestamp

Project:

project_name: Name of the project
client: Associated client (Foreign Key)
created_by: User who created the project
users: Many-to-many relationship with assigned users
created_at: Creation timestamp
updated_at: Last update timestamp

Installation & Setup:

Clone the repository (if using version control)

Install dependencies: The project uses Django and Django REST Framework. Dependencies are managed through Django's package system.


Create a superuser:
python manage.py createsuperuser

Run migrations:
python manage.py makemigrations
python manage.py migrate

Start the development server:
python manage.py runserver 0.0.0.0:5000