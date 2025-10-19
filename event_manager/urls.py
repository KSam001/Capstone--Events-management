from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet # The correct class name is imported
from django.views.generic import TemplateView 

# Setup DRF Router for Event CRUD
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/', include('users.urls')),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # FRONTEND LANDING PAGE (Serves index.html at the root)
    path('', TemplateView.as_view(template_name='index.html')), 
]
