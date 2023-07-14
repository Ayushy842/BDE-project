from django.contrib import admin
from app.models import BDE_User,Project,Round1,Round2,Round3
# Register your models here.
admin.site.register([BDE_User])
admin.site.register(Project)
admin.site.register(Round1)
admin.site.register(Round2)
admin.site.register(Round3)