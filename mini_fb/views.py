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
