from django.urls import path
from django.contrib.auth.views import LogoutView
from main.views import *

urlpatterns = [
    path('', ChallengesView.as_view(), name = 'challenges'),
    path('challenges/<int:pk>', ChallengeView.as_view(), name = 'challenge'),
    path('create-submission/', CreateSubmissionView.as_view(), name='create_submission'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]