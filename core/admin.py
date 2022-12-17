from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('id', 'first_name', 'last_name', 'birth', 'phone', 'is_male', 'bio', 'profile_img', 'cover_img',
                                        'location', 'education', 'code', 'privacy')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Skill)
admin.site.register(User_Skill)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Post_Tag)
admin.site.register(Post_Img)
admin.site.register(Post_Video)
admin.site.register(Post_Like)
admin.site.register(Post_Comment)
admin.site.register(Comment_Img)
admin.site.register(Comment_Vid)
admin.site.register(Post_Comment_Reply)
