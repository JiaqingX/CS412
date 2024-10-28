from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_queryset(self):

        if Profile.objects.count() == 0:
            Profile.objects.create(first_name="Elon", last_name="Musk", city="Austin", profile_image_url="https://assets-us-01.kc-usercontent.com/5cb25086-82d2-4c89-94f0-8450813a0fd3/0c3fcefb-bc28-4af6-985e-0c3b499ae832/Elon_Musk_Royal_Society.jpg?fm=jpg&auto=format")
            Profile.objects.create(first_name="Taylor", last_name="Swift", city="Nashville", profile_image_url="https://m.media-amazon.com/images/M/MV5BYWYwYzYzMjUtNWE0MS00NmJlLTljNGMtNzliYjg5NzQ1OWY5XkEyXkFqcGc@._V1_.jpg")
            Profile.objects.create(first_name="Cristiano", last_name="Ronaldo", city="Lisbon", profile_image_url="https://hips.hearstapps.com/hmg-prod/images/cristiano-ronaldo-of-portugal-reacts-as-he-looks-on-during-news-photo-1725633476.jpg?crop=0.666xw:1.00xh;0.180xw,0&resize=640:*")
            Profile.objects.create(first_name="Oprah", last_name="Winfrey", city="Chicago", profile_image_url="https://www.penfaulkner.org/wp-content/uploads/2022/03/Hi-Res_OW-Headshot_Harpo-Inc.Chris-Craymer-scaled.jpg")
            Profile.objects.create(first_name="Emma", last_name="Watson", city="London", profile_image_url="https://cdn.britannica.com/29/215029-050-84AA8F39/British-actress-Emma-Watson-2017.jpg")


        return Profile.objects.all()

from django.views.generic import DetailView
from .models import Profile


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Profile
from .forms import CreateProfileForm

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})

from django.urls import reverse
from django.views.generic import CreateView
from .models import Profile, StatusMessage, Image
from .forms import CreateStatusMessageForm
from django.shortcuts import get_object_or_404


class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):

        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        
        sm = form.save(commit=False)
        
        sm.profile = profile

        sm.save()

        files = self.request.FILES.getlist('files')

        for f in files:
            image = Image(status_message=sm, image_file=f)
            image.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile 
        return context

    def get_success_url(self):

        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})


from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import StatusMessage

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})


from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import StatusMessage

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']  
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})


from django.urls import reverse
from django.views.generic import UpdateView
from .models import Profile
from .forms import UpdateProfileForm

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

from django.shortcuts import redirect
from django.views import View

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other_profile = Profile.objects.get(pk=self.kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

from django.views.generic import DetailView
from .models import Profile

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context

from django.views.generic import DetailView
from .models import Profile

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()  
        return context
