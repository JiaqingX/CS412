import random
from datetime import datetime, timedelta
from django.shortcuts import render

def confirmation(request):
    if request.method == 'POST':
   
        items = request.POST.getlist('menu_items')
        customer_name = request.POST.get('customer_name')
        total_price = sum([int(price) for price in request.POST.getlist('price')])

 
        ready_time_delta = random.randint(30, 60) 
        ready_time = datetime.now() + timedelta(minutes=ready_time_delta)
        ready_time_formatted = ready_time.strftime('%H:%M')  


        context = {
            'items': items,
            'customer_name': customer_name,
            'total_price': total_price,
            'ready_time': ready_time_formatted,
        }

 
        return render(request, 'restaurant/confirmation.html', context)
