from django.contrib import admin
from .models import CustomUser,Poll,Choice,Vote

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)
