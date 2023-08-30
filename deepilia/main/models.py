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
