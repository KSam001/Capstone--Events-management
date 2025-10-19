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

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

* Python 3.8+
* `pip` and `venv` (or `conda`)

### 1. Setup Environment and Dependencies

```bash
# Clone the repository
git clone [https://github.com/KSam001/Capstone--Events-management.git](https://github.com/KSam001/Capstone--Events-management.git)
cd Capstone--Events-management

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
