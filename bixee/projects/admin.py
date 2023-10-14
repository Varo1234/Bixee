from django.contrib import admin
from .models import Projects, UserProfile, Tasks


class UserProfileAdmin(admin.ModelAdmin):
    image_fields = ('image',)


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_finalizacion',)
    list_filter = ('fecha_inicio', 'fecha_finalizacion',)
    search_fields = ('nombre', 'descripcion',)
    date_hierarchy = 'fecha_inicio'
    filter_horizontal = ('tasks',)


class TasksAdmin(admin.ModelAdmin):
    list_display = ('name', 'completed',)
    list_filter = ('completed',)
    search_fields = ('name', 'description',)
    filter_horizontal = ('assigned_to',)


admin.site.register(Projects, ProyectoAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tasks, TasksAdmin)

