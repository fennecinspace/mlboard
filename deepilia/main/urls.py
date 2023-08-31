from django.urls import path, include

from main import views

urlpatterns = [
    path('', views.team_view, name='team'),
    path('team/', views.team_view, name='team'),
    path('team/<str:username>/', views.ProfileView.as_view(), name='profile'),
    
	path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('apps/', views.AppsView.as_view(), name='apps'),
]