# Capstone: Event Management API 🗓️

This project is a robust, production-ready RESTful API and a functional, integrated simple **HTML/CSS/JS frontend** for managing user accounts, creating events, and handling RSVPs. The project is built using **Django** and **Django REST Framework (DRF)**.

The entire project is structured as a single deployable unit, with the Django backend serving the simple frontend for easy demonstration and deployment.

## 🌟 Features

* **User Authentication:** Secure registration and login using **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.
* **User Profile Management:** Users can view and update their own profile information.
* **Event Management (CRUD):** Authenticated users can create, read, update, and delete their own events.
* **RSVP System:** Authenticated users can RSVP to any event, or cancel an existing RSVP.
* **API Structure:** All core logic is exposed via clean, documented RESTful endpoints.
* **Integrated Frontend:** A basic HTML/CSS/JS frontend is served at the root `/` URL for immediate visualization and interaction with the API.

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend Framework** | Django | Core web framework |
| **API** | Django REST Framework (DRF) | Building the RESTful API endpoints |
| **Authentication** | djangorestframework-simplejwt | Handling secure JWT access and refresh tokens |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) | Simple interface for testing and visualization |
| **Database** | SQLite (Default), PostgreSQL ready | Data persistence and management |

Capstone: Scalable Events Management API
🚀 Project Overview
The Events Management API is a robust, production-ready backend built using Django and the Django REST Framework (DRF). It serves as the core service for a modern full-stack events platform, providing secure, structured access to event and user data via RESTful endpoints.

The primary objectives of this project were to implement best practices in:

Custom User Authentication using JSON Web Tokens (JWT).

Scalable Application Structure with separated functional apps (users, events).

Cloud Deployment using Gunicorn, Whitenoise, and environment-specific configuration (runtime.txt, Procfile).

⚙️ Core Architecture and Tenets
The project is segmented into distinct applications and configuration files, each with a single, clear responsibility.


Project Configuration	
| **Component** | **Path / Tool** | **Description** |
|----------------|------------------|------------------|
| **Core Project Folder** | `Capstone_Events_management/` | Houses the global settings (`settings.py`), URL routing (`urls.py`), and the WSGI entry point for the production server (`wsgi.py`). |
| **Authentication & Users** | `users/` App | Manages the Custom User Model. Handles user registration, custom fields, and ensures email is the primary login credential. |
| **Events Business Logic** | `events/` App | Core API functionality. Defines the `Event` and related models (e.g., `Registration`), and implements the DRF ViewSets for full CRUD operations. |
| **Frontend Integration** | `frontend/` Folder | Contains the separate client-side code (e.g., React, Vue) that consumes the API endpoints, ensuring a clear separation of concerns. |
| **JWT Authorization** | Implemented via `simplejwt` | Provides stateless, token-based security. Handles token generation (`/api/token/`), refresh, and validation for all protected endpoints. |
| **Deployment Setup** | `Procfile`, `runtime.txt` | Defines the production environment. `Procfile` specifies the Gunicorn start command, while `runtime.txt` locks the Python version (`python-3.12.4`). |





🔑 API Reference and Authentication
The API uses JSON Web Tokens (JWT) for secure, authorized access to protected endpoints.

1. Token Acquisition
To access event management features, you must first obtain an access token.

Action	Endpoint	Method	Required Payload
Register User	/api/users/register/	POST	email, password
Obtain Tokens	/api/token/	POST	email, password
Refresh Token	/api/token/refresh/	POST	refresh (token)



2. Events Endpoints (Protected)
All calls to the following endpoints must include the Authorization header with the format: Authorization: Bearer <ACCESS_TOKEN>.

Endpoint	Method	Description
/api/events/	GET	List all available events.
/api/events/	POST	Create a new event. Requires event data (title, date, location, etc.).
/api/events/<id>/	GET	Retrieve details for a specific event.
/api/events/<id>/	PUT/PATCH	Update a specific event (Owner only).
/api/events/<id>/	DELETE	Delete a specific event (Owner only).



💻 Local Setup and Installation
Follow these steps to get the API running on your local machine.

Prerequisites
Python 3.12+

pip and venv (recommended)

PostgreSQL or SQLite (default)

Installation Steps
Clone the Repository

Bash

git clone https://github.com/KSam001/Capstone--Events-management.git
cd Capstone--Events-management
Create and Activate Virtual Environment

Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

Bash

pip install -r requirements.txt
Configure Environment Variables

Create a file named .env in the project root and add the following:

Code snippet

SECRET_KEY='your_super_secret_key_here'
DEBUG=True
# Use SQLite for simple local setup
DATABASE_URL=sqlite:///db.sqlite3 
Run Database Migrations

Apply the schema changes for the users and events apps.

Bash

python manage.py makemigrations
python manage.py migrate
Create a Superuser (Admin)

Bash

python manage.py createsuperuser
Start the Development Server

Bash

python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

🌐 Deployment Notes
This project is configured for deployment using a WSGI server and static file handling middleware.

Component	Purpose	Details
Gunicorn	Production WSGI Server	Defined in the Procfile to handle concurrent requests efficiently.
Whitenoise	Static File Serving	Handles the serving of static assets (CSS, JS) in a production environment, improving performance and reliability.
wsgi.py Path Fix	Deployment Stability	The final commit (34c20bf) adjusted the path in wsgi.py to ensure correct import resolution, a critical fix for nested Django project structures on cloud hosts.

