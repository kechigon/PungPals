from django.contrib import admin

from .models import CustomUser, Room, Taikyoku3, Taikyoku4, Senseki3, Senseki4


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(Taikyoku3)
admin.site.register(Taikyoku4)
admin.site.register(Senseki3)
admin.site.register(Senseki4)