from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from accounts.forms import SignupForm, ProfileForm
from .models import Accounts

admin.site.register(Accounts)

User = get_user_model()

# @admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = SignupForm
    add_form = ProfileForm
    fieldsets = (("User", {"fields": ("name","following",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]