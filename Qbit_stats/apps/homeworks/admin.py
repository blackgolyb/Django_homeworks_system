from django.contrib import admin
from homeworks.models import Homework, CompliteHomework, Topic

admin.site.register(Topic)
admin.site.register(Homework)
admin.site.register(CompliteHomework)

# Register your models here.
