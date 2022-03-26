from django.contrib import admin
from . import models
from .models import child, kid_meal
# Register your models here.

admin.site.register(child)
admin.site.register(kid_meal)
