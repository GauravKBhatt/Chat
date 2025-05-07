from django.contrib import admin
from .models import *

admin.register(CustomUserManager)
admin.register(User)