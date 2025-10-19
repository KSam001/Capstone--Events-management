# Event Management API

## Project Overview

The **Event Management API** is a robust RESTful service designed to allow users to create, manage, and RSVP to events. Built using **Django** and **Django REST Framework (DRF)**, the API provides a secure and scalable backend for any event-based application, focusing on user management, model relationships, and detailed access control.

---

## 🚀 Key Features

* **User Management:** Secure registration, login, and profile management using **email as the primary authentication field**.
* **Event CRUD:** Authenticated users can create, view, update, and delete events.
* **Access Control:** Only the event host can modify or delete their events.
* **Event RSVP System:** Users can easily RSVP to an event and view the list of attendees.
* **Public Listings:** View a complete list of upcoming events available to all users.

---

## 🛠️ Technology Stack

* **Backend Framework:** Django
* **API Framework:** Django REST Framework (DRF)
* **Database:** PostgreSQL (Recommended for production) / SQLite (Default for development)
* **Authentication:** Token-based Authentication

---

## 💡 API Endpoints

The API is structured around two main apps: `users` and `events`. All endpoints are prefixed with `/api/`.

### User Endpoints (`users` app)

| Method | Endpoint | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/register/` | Create a new user account. | None |
| `POST` | `/api/login/` | Log in and receive an authentication token. | None |
| `GET/PUT` | `/api/profile/` | View/update the authenticated user's profile. | Token Required |

### Event Endpoints (`events` app)

| Method | Endpoint | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `GET/POST` | `/api/events/` | List all events or create a new event. | POST requires Token |
| `GET/PUT/DELETE` | `/api/events/<id>/` | Retrieve, update, or delete a specific event. | PUT/DELETE requires Host Token |
| `POST` | `/api/events/<id>/rsvp/` | RSVP to an event (toggle attendance). | Token Required |
| `GET` | `/api/events/<id>/attendees/` | View a list of users who have RSVP'd. | Any User |

---
