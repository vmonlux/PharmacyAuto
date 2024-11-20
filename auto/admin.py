from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from auto.models import *
from auto.forms import *

admin.site.register(User)
admin.site.register(Omnicell)
admin.site.register(Refrigerator)
admin.site.register(OmnicellModel)
admin.site.register(Site)
admin.site.register(Building)
admin.site.register(Aux)
admin.site.register(Lockbox)
admin.site.register(RefrigeratorModel)
