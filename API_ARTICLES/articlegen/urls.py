from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ArticleViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
