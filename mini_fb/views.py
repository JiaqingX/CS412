from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile, StatusMessage, Friend, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user == self.object.user:
            context['form'] = CreateStatusMessageForm()
        else:
            context['not_owner'] = True
        return context

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
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('show_profile', pk=profile.pk)
        
        return render(request, 'mini_fb/create_profile_form.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        if self.request.user != profile.user:
            return redirect('show_profile', pk=profile.pk)
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

class ShowFriendSuggestionsView(LoginRequiredMixin, View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        friend_suggestions = profile.get_friend_suggestions()
        return render(request, 'mini_fb/friend_suggestions.html', {
            'profile': profile,
            'friend_suggestions': friend_suggestions
        })

class ShowNewsFeedView(LoginRequiredMixin, View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        news_feed = profile.get_news_feed()
        return render(request, 'mini_fb/news_feed.html', {
            'profile': profile,
            'news_feed': news_feed
        })

class CreateFriendView(LoginRequiredMixin, View):
    def post(self, request, other_pk):
        profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=other_pk)
        if profile != other_profile:
            profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

# DeleteStatusMessageView remains unchanged
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})
