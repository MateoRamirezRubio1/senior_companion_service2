from django.contrib import admin
from .models import Customer, MedicalInformation, Preference

admin.site.register(Customer)
admin.site.register(MedicalInformation)
admin.site.register(Preference)
