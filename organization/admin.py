from django.contrib import admin
from . import models


admin.site.register(models.Department)
admin.site.register(models.Program)
admin.site.register(models.Course)
