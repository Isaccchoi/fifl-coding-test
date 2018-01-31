from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('user_id', 'password', 'name', 'is_admin')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    list_display = ('user_id', 'name', 'phone_number', 'is_admin')
    list_filter = ('is_active', 'is_admin',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'name', 'phone_number', 'password1', 'password2')}
         ),
    )
    search_fields = ('user_id',)
    ordering = ('user_id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
