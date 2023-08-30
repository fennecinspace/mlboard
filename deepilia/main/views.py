from typing import Any, Optional
from django.db import models
from django.shortcuts import render
from django.views.generic import DetailView
from main.models import Member

# Create your views here.

def team_view(request):
	context = {
		'professors': Member.objects.filter(rank = "Professor"),
		'allums': None,
		'phds': Member.objects.filter(rank = "PhD Student"),
		'postdocs': None,
		'collaborators': None,
		'engineers': Member.objects.filter(rank = "Engineer"),
	}
	return render(request, 'team.html', context)

class ProfileView(DetailView):
	model = Member
	template_name = 'profile.html'

	def get_object(self):
		return self.model.objects.get(
			user__username = self.kwargs.get("username")
		)