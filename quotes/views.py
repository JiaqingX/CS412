import random
from django.shortcuts import render

# List of quotes and images
quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Your time is limited, so don’t waste it living someone else’s life. - Steve Jobs",
    "Stay hungry, stay foolish. - Steve Jobs",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "Design is not just what it looks like and feels like. Design is how it works. - Steve Jobs"
]

images = [
    "/static/images/1.jpg",
    "/static/images/2.jpg", 
    "/static/images/3.jpg", 
    "/static/images/4.jpg", 
    "/static/images/5.jpg",   

]

# View for displaying a random quote and image
def quote(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    context = {'quote': selected_quote, 'image': selected_image}
    return render(request, 'quote.html', context)

# View for showing all quotes and images
def show_all(request):
    context = {'quotes': quotes, 'images': images}
    return render(request, 'show_all.html', context)

# About page view
def about(request):
    return render(request, 'about.html')
