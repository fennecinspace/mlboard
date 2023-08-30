from django.urls import path, include

from main import views

urlpatterns = [
    path('team/', views.team_view, name='team'),
    path('team/<str:username>/', views.ProfileView.as_view(), name='profile'),

	# path('', views.home_view, name='home'),
	# path('<int:year>', views.home_view, name='home_per_year'),

	# path('programme/', views.program_view, name='program'),
	# path('programme/<int:year>', views.program_view, name='program_per_year'),

	# path('prix/', views.prix_view, name='prix'),
	# path('prix/<int:year>', views.prix_view, name='prix_per_year'),

	# path('apps/', views.apps_view, name='apps'),
	# path('apps/<int:year>', views.apps_view, name='apps_per_year'),
	
	# path('comite/<int:year>', views.comite_view, name='comite_per_year'),

	# path('priticipants/', views.priticipants_view, name='priticipants'),
	# path('priticipants/<int:year>', views.priticipants_view, name='priticipants_per_year'),

	
	# path('workshop_registration', views.workshop_registration_view, name='workshop_registration'),
	# path('app/<int:pk>', views.AppView.as_view(), name='app'),
	# path('accounts/', include('allauth.urls')),
	# path('send_emails', views.send_emails_view, name='send_emails'),
	# path('submit_emails', views.submit_emails_view, name='submit emails'),
]