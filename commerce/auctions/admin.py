from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(User, UserAdmin)