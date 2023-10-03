from django.urls import path, include

from main import views

urlpatterns = [
    path('', views.main_view, name='home'),
    path('team/', views.team_view, name='team'),
    path('team/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('news/<pk>/', views.PostDetailView.as_view(), name='news'),
	path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('apps/', views.AppsView.as_view(), name='apps'),
]