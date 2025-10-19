from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProfileView

urlpatterns = [
    # JWT Login: POST to /api/token/
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registration: POST to /api/register/
    path('register/', RegisterView.as_view(), name='api_register'),
    
    # Profile endpoint: GET/PUT to /api/profile/
    path('profile/', ProfileView.as_view(), name='api_profile'),
]
