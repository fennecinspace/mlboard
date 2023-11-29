from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.auth.models import User

from main.models import *

class ChallengesView(ListView):
    model = Challenge
    template_name = 'challenges.html'

class ChallengeView(DetailView):
    model = Challenge
    template_name = 'challenge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenge_variants = ChallengeVariant.objects.filter(challenge = context['object'])
        context['challenge_variants'] = challenge_variants

        # Fetch the authenticated user's submissions
        user_submissions = Submission.objects.filter(
            challenge__in=challenge_variants,
            user=self.request.user
        ).order_by('-score')

        all_submissions = Submission.objects.filter(challenge__in = challenge_variants, status = 'DONE')

        # Fetch the best submission per user
        best_submissions = {}

        for submission in all_submissions:
            if submission.score:
                if submission.user not in best_submissions:
                    best_submissions[submission.user] = submission
                elif submission.score > best_submissions[submission.user].score:
                    best_submissions[submission.user] = submission

        submissions = [sub.id for user, sub in best_submissions.items()]

        best_submissions = Submission.objects.filter(id__in = submissions).order_by('-score')  

        context['user_submissions'] = user_submissions
        context['best_submissions'] = best_submissions
        
        return context


class CustomLoginView(LoginView):
    template_name = 'login.html'


class CreateSubmissionView(View):
    def post(self, request):
        challenge_variant_id = request.POST.get('challenge_variant')
        uploaded_file = request.FILES['file']
        # Handle file upload, processing, and score calculation here.
        # Create a new Submission object and save it.

        challenge_variant = ChallengeVariant.objects.filter(id = challenge_variant_id)[0]
        Submission(user = request.user, challenge = challenge_variant, file = uploaded_file).save()

        return redirect('challenge', pk = challenge_variant.challenge.pk)


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User  # Replace with your user model if needed


class ChangePasswordView(PasswordChangeView):
    template_name = 'change_password.html'
    form_class = ChangePasswordForm
    success_url = '/change_password/'  # Redirect to the same page

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")

        messages.error(self.request, 'There was an error changing your password. Please check the following: ' + ', '.join(error_messages))
        return super().form_invalid(form)