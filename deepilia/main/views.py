from django.shortcuts import render

# Create your views here.

def team_view(request):
	context = {
		'professors': None,
		'allums': None,
		'phds': None,
		'postdocs': None,
		'collaborators': None,
	}
	return render(request, 'team.html', context)