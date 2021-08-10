from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from apps.user.forms import UserChangeForm, UserCreationForm
from .models import UserLoginActivity ,CreateAccount, User
from import_export.admin import ImportExportModelAdmin

from django.utils.translation import gettext_lazy as _

# User = get_user_model()


@admin.register(CreateAccount)
class CreateAccountAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name','email','password','pro',"move","months")
    list_filter = ('pro',"move",)
    readonly_fields = ('password','pro',)

    fieldsets = (
        (_('ORG'), {'fields': ('org_auto', 'org_name',)}),
        (_('Main'), {'fields': ('name', 'email','move', )}),
        (_('Keywords'), {'fields': ('keywords', 'keywords_tm','months',)}),
        (_('ITI'), {'fields': ('branch', 'state',)}),
    )
    search_fields = ('name',)


@admin.register(UserLoginActivity)
class UserLoginActivityAdmin(admin.ModelAdmin):
    search_fields = ('login_IP','login_username',)
    list_display = ('login_IP','login_datetime','login_username','status',)
    list_filter = ('login_datetime','login_username','login_IP',)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),)  
    list_display = ["id","username", "name", "is_superuser"]
    search_fields = ["name","email",]


    def save_model(self, request, obj, form, change):
        obj.save()
        # reset_all()
