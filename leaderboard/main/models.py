import os
import zipfile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Challenge(models.Model):
	title = models.CharField(max_length=512, null=True, blank=True)
	description = models.TextField(max_length=3000, blank=True)
	image = models.ImageField(null=True, blank=True)
	files = models.ManyToManyField("Resource", blank=True)

	def __str__(self):
		return self.title


class ChallengeVariant(models.Model):
	title = models.CharField(max_length=512, null=True, blank=True)
	challenge = models.ForeignKey('Challenge', on_delete = models.CASCADE)
	processor = models.ForeignKey('Processor', on_delete = models.CASCADE)

	def __str__(self):
		return f"{self.challenge.title} {self.title}"


class Resource(models.Model):
	name = models.CharField(max_length=200)
	file = models.FileField(upload_to='files/', null=True, blank=True)
	url = models.URLField(null=True, blank=True)
   
	def __str__(self):
		return self.name


# method for updating
@receiver(post_save, sender=Resource, dispatch_uid="unzip_files")
def update_stock(sender, instance, **kwargs):
	if zipfile.is_zipfile(instance.file.path):
		print('it is a zip file')
		with zipfile.ZipFile(instance.file.path, 'r') as zip_ref:
			extract_to_dir = instance.file.path.split('.zip')[0]
			if not os.path.exists(extract_to_dir): 
				os.makedirs(extract_to_dir) 
			zip_ref.extractall(extract_to_dir)


class Submission(models.Model):
	user = models.ForeignKey("auth.User", on_delete = models.CASCADE)
	challenge = models.ForeignKey("ChallengeVariant", on_delete = models.CASCADE)
	file = models.FileField(upload_to ='submissions/')
	score = models.FloatField(blank = True, null = True)
	status = models.CharField(max_length = 200, choices = (
		('ERROR', 'ERROR'),
		('PROCESSING', 'PROCESSING'),
		('IN-QUEUE', 'IN-QUEUE'),
		('DONE', 'DONE'),
	), default = 'IN-QUEUE')

	def filename(self):
		return os.path.basename(self.file.name)

	def __str__(self):
			return f"{self.user.username} {self.challenge.title} {self.score}"


class Processor(models.Model):
	image_name = models.CharField(max_length = 512)
	command = models.CharField(max_length = 512)

	def __str__(self):
		return self.command