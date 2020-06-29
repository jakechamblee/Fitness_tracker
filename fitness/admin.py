from django.contrib import admin
from .models import Exercise, ExerciseInstance, Workout


class ExerciseInstanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_performed', 'name')
    list_filter = ('user', 'date_performed', 'name')


admin.site.register(Exercise)
admin.site.register(ExerciseInstance, ExerciseInstanceAdmin)
admin.site.register(Workout)
