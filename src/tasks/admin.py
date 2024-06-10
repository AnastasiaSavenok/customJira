from django.contrib import admin

from src.tasks.models import Task

admin.site.register(Task)
