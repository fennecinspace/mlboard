from django.contrib import admin
from main.models import Member, Thesis, Project, Partner, Application, Post


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'rank', 'website', 'github', 'linkedin', 'picture']
    
    @admin.display(ordering='id', description='Full Name')
    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ['title', 'phd', 'image']
    
    @admin.display(description='PhD')
    def phd(self, obj):
        student = Member.objects.filter(thesis = obj)
        return student [0] if student.__len__() else None


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'website']
    
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'youtube_video_code', 'github']
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'header']
    