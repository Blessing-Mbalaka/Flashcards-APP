from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'decks', views.DeckViewSet, basename='deck')
router.register(r'flashcards', views.FlashcardViewSet, basename='flashcard')
router.register(r'sessions', views.StudySessionViewSet, basename='session')

app_name = 'flashcards'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/profile/', views.UserProfileView.as_view(), name='profile'),
]
