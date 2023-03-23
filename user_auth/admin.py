from django.contrib import admin
from app.models import *
from user_auth.models import User_data
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class UserModelAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name','contact_no','date_of_birth','address','work_field', 'is_admin','is_verified')
    list_filter = ('is_admin', 'work_field',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',
         'last_name', 'address','date_of_birth', 'work_field', 'contact_no','upload_image','upload_id_proof','is_verified','is_active')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'contact_no','address', 'work_field', 'password1'),
        }),
    )
    search_fields = ('email','address', 'work_field',)
    ordering = ('email', 'id')
    filter_horizontal = ()


# # Now register the new UserModelAdmin...
admin.site.register(User_data, UserModelAdmin)
admin.site.register(Job)
admin.site.register(BidForJob)
admin.site.register(UserFeedback)
