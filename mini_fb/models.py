from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Profile model


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    profile_image_url = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')
    
    def get_friends(self):
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = list(friends1) + list(friends2)
        return Profile.objects.filter(id__in=friend_ids)
    
    def add_friend(self, other):
        if not Friend.objects.filter(
            (models.Q(profile1=self) & models.Q(profile2=other)) |
            (models.Q(profile1=other) & models.Q(profile2=self))
        ).exists() and self != other:
            Friend.objects.create(profile1=self, profile2=other)

    def get_news_feed(self):
        friend_ids = [friend.pk for friend in self.get_friends()]
        return StatusMessage.objects.filter(profile__in=friend_ids + [self.pk]).order_by('-timestamp')
    
    def get_friend_suggestions(self):
        friends = self.get_friends()  
        exclude_ids = [self.id] + [friend.id for friend in friends]  

        return Profile.objects.exclude(id__in=exclude_ids)



class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f'{self.message[:20]}...'

    def get_images(self):
        return self.images.all().order_by('timestamp')

# Image model
class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(default=timezone.now)
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.status_message} at {self.timestamp}"

# Friends Model
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"