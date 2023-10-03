from django.db import models

class Member(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)
    bio = models.TextField(max_length=3000, blank=True)
    research_interest = models.CharField(max_length=256, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    funding_info = models.CharField(max_length=256, null=True, blank=True)
    rank = models.CharField(max_length=20, choices=(
        ('Professor', 'Professor',),
        ('PhD Student', 'PhD Student',),
        ('Engineer', 'Engineer',),
        ('Other', 'Other',)
    ), default = "PhD Student")

    thesis = models.OneToOneField('Thesis', on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"  

class Thesis(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(max_length=3000, blank=True)
    keywords = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    advisors = models.ManyToManyField('Member', blank=True, related_name = "supervisions")
    
    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(max_length=3000, blank=True)
    image = models.ImageField(null=True, blank=True)
    partners = models.ManyToManyField('Partner', blank=True)
    managers = models.ManyToManyField('Member', blank=True, related_name = 'managers')
    researchers = models.ManyToManyField('Member', blank=True, related_name = 'researchers')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Partner(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Application(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)
    short_description = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(max_length=3000, blank=True)
    youtube_video_code = models.CharField(max_length=20, null=True, blank=True)
    github = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    title = models.CharField(max_length=1024)
    header = models.ImageField()
    short_content = models.TextField(max_length=2048)
    content = models.TextField(max_length=10000)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title