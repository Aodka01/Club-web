# Register your models here.
from django.contrib import admin
from .models import Club, Membership, Event

admin.site.register(Club)
admin.site.register(Membership)
admin.site.register(Event)