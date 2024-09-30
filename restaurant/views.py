from django.shortcuts import render
import random

# View for the main page
def main(request):
    return render(request, 'restaurant/main.html')

# View for the order page
def order(request):
    daily_special = random.choice(['Pizza', 'Pasta', 'Burger', 'Salad'])
    context = {'daily_special': daily_special}
    return render(request, 'restaurant/order.html', context)

# View for the confirmation page
def confirmation(request):
    if request.method == 'POST':
        items = request.POST.getlist('menu_items')
        customer_name = request.POST.get('customer_name')
        total_price = sum([int(price) for price in request.POST.getlist('price')])

        # Calculate random ready time (between 30-60 minutes)
        import time
        ready_time = time.strftime('%H:%M', time.localtime(time.time() + random.randint(30, 60) * 60))

        context = {
            'items': items,
            'customer_name': customer_name,
            'total_price': total_price,
            'ready_time': ready_time,
        }
        return render(request, 'restaurant/confirmation.html', context)
