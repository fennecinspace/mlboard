from typing import Any, Optional
from django.db import models
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from main.models import Member, Application, Project, Post

# Create your views here.

def team_view(request):
	context = {
		'professors': Member.objects.filter(rank = "Professor"),
		'allums': None,
		'phds': Member.objects.filter(rank = "PhD Student"),
		'postdocs': None,
		'collaborators': Member.objects.filter(rank = "Other"),
		'engineers': Member.objects.filter(rank = "Engineer"),
	}
	return render(request, 'team.html', context)

def main_view(request):
	context = {
		'news': Post.objects.all(),
	}
	return render(request, 'home.html', context)

class ProfileView(DetailView):
	model = Member
	template_name = 'profile.html'

	def get_object(self):
		return self.model.objects.get(
			user__username = self.kwargs.get("username")
		)
	
class AppsView(ListView):
	model = Application
	template_name = 'apps.html'

class ProjectsView(ListView):
	model = Project
	template_name = 'projects.html'
	

class PostDetailView(DetailView):
	model = Post
	template_name = 'post.html'
	context_object_name = 'post'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context