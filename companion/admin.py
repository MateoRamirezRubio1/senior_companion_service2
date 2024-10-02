from django.contrib import admin
from .models import Companion, Certification, Reference, Skill, TimeAvailability

admin.site.register(Companion)
admin.site.register(Certification)
admin.site.register(Reference)
admin.site.register(Skill)
admin.site.register(TimeAvailability)
