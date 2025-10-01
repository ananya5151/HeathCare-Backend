from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, DoctorViewSet, PatientViewSet, PatientDoctorMappingViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet, basename='patient') # We use basename because the queryset is customized
router.register(r'mappings', PatientDoctorMappingViewSet)

# The API URLs are now determined automatically by the router.
# The auth URLs are added manually.
urlpatterns = [
    # Auth URLs
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API URLs
    path('', include(router.urls)),
]