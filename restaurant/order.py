import random
from django.shortcuts import render

def order(request):
    daily_special = random.choice(['Pizza', 'Pasta', 'Burger', 'Salad'])
    context = {'daily_special': daily_special}
    return render(request, 'restaurant/order.html', context)
