from django.contrib import admin
from .models import User, Language, LanguageUser

admin.site.register(User)
admin.site.register(Language)
admin.site.register(LanguageUser)
