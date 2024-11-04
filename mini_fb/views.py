from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile, StatusMessage, Friend, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm

# Show all profiles
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

# Show individual profile page
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is authenticated and if they are viewing their own profile
        if self.request.user.is_authenticated and self.request.user == self.object.user:
            context['form'] = CreateStatusMessageForm()  # Pass the CreateStatusMessageForm to the template
        else:
            context['not_owner'] = True  # Add a flag for non-owners
        return context

# Create new profile
class CreateProfileView(View):
    def get(self, request):
        user_form = UserCreationForm()
        profile_form = CreateProfileForm()
        return render(request, 'mini_fb/create_profile_form.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user  # Link the user to the profile
            profile.save()
            login(request, user)  # Log the user in immediately after signup
            return redirect('show_profile', pk=profile.pk)
        
        return render(request, 'mini_fb/create_profile_form.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

# Create new status message
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        if self.request.user != profile.user:
            return redirect('show_profile', pk=profile.pk)  # Redirect if not the owner
        sm = form.save(commit=False)
        sm.profile = profile
        sm.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image(status_message=sm, image_file=f)
            image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

# Delete status message
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

# Update status message
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

# Update profile view
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

# Add friend view
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other_profile = Profile.objects.get(pk=self.kwargs['other_pk'])
        if request.user == profile.user:
            profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

# Friend suggestions view
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context

# News feed view
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context


from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'