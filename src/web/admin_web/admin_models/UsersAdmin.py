from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.models import Users


@admin.register(Users, site=admin_site)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "fullname", "is_admin", "locale", "created_at")
    list_filter = ("is_admin", "locale")
    readonly_fields = ("id", "username", "fullname", "created_at")

    # search_fields = ()
    # list_editable = ()

    def has_add_permission(self, request):
        return False
