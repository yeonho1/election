from django.contrib import admin
from .models import VoteTopic, VoteSelection

# Register your models here.

admin.site.register(VoteTopic)
admin.site.register(VoteSelection)