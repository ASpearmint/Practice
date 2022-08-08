from django.contrib import admin
from .models import *

# Register your models here.

register = admin.site.register

register(User)
register(Email)