from django.contrib import admin
from .models import User, Article
from django.core.exceptions import PermissionDenied


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role')
    fields = ('email', 'role', 'password')

    # Customizationn

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and obj.role == 'author':
            raise PermissionDenied("Only admins can assign the 'Author' role.")
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
admin.site.register(Article)
