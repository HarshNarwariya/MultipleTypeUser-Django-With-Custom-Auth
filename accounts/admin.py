from django.contrib import admin
from accounts.models import User, Reader, Writter, WritterMore

add_user_fieldsets = (
    ('Personal Information', {
        'fields': ('email', 'first_name', 'last_name'),
    }),
    ('Verify Password', {
        'fields': ('password',),
        'description': "You change your password right from here. Password given below is hashed!",
    }),
    ('Permissions', {
        'fields': ('groups', 'user_permissions')
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
    filter_horizontal = ('groups', 'user_permissions',)

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = Writter.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        return super().save_model(request, obj, form, change)
    
@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    fieldsets = add_user_fieldsets
    filter_horizontal = ('groups', 'user_permissions',)

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = Reader.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        return super().save_model(request, obj, form, change)

