import random
import time
from django.shortcuts import render

def confirmation(request):
    if request.method == 'POST':
        items = request.POST.getlist('menu_items')
        customer_name = request.POST.get('customer_name')
        total_price = sum([int(price) for price in request.POST.getlist('price')])

        # Calculate random ready time (between 30-60 minutes)
        ready_time = time.strftime('%H:%M', time.localtime(time.time() + random.randint(30, 60) * 60))

        context = {
            'items': items,
            'customer_name': customer_name,
            'total_price': total_price,
            'ready_time': ready_time,
        }
        return render(request, 'restaurant/confirmation.html', context)
