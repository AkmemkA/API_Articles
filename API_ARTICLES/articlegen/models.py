from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied


class User(AbstractUser):
    ROLE_CHOICES = [
        ('subscriber', 'Subscriber'),
        ('author', 'Author'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,
                            default='subscriber')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='articles',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:  # New article
            if self.author.role != 'author':
                raise PermissionDenied("Only authors can create articles.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.author.role != 'author':
            raise PermissionDenied("Only authors can delete articles.")
        super().delete(*args, **kwargs)


