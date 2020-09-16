from django.contrib import admin

# Register your models here.
from homeworkday05 import models

admin.site.register(models.Teacher)
admin.site.register(models.Course)
admin.site.register(models.User)
