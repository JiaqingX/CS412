from django.db import models
from django.utils import timezone

# Profile model
class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')


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
