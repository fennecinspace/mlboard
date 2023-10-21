from django.contrib import admin
from main.models import *
# Register your models here.


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(ChallengeVariant)
class ChallengeVariantAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge', 'processor']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'score', 'status']

@admin.register(Processor)
class ProcessorAdmin(admin.ModelAdmin):
    pass