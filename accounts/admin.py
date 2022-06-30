from django.contrib import admin
from accounts.models import User, Reader, Writter, WritterMore

add_user_fieldsets = (
    ('Personal Information', {
        'fields': ('email', 'first_name', 'last_name'),
    }),
    ('Verify Password', {
        'fields': ('password',),
    }),
    ('Permissions', {
        'fields': ('user_permissions', 'groups'),
    }),
    ('User Access', {
        'fields': ('is_active', 'is_admin', 'is_superuser'),
    })
)

# Register your models here.
class WritterMoreInline(admin.StackedInline):
    model = WritterMore


@admin.register(Writter)
class WritterAdmin(admin.ModelAdmin):
    fieldsets = add_user_fieldsets
    inlines = (WritterMoreInline,)
    
@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    fieldsets = add_user_fieldsets


