from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Article
from .serializers import UserSerializer, ArticleSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'subscriber':
            return Article.objects.all()
        return Article.objects.filter(is_private=False)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['put', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def update_or_delete(self, request, pk=None):
        article = self.get_object()
        if article.author != request.user and request.user.role != 'author':
            return Response(
                {"detail": "Not authorized to edit or delete this article."},
                status=403)

        if request.method == 'PUT':
            return self.update(request, pk)
        elif request.method == 'DELETE':
            return self.destroy(request, pk)
