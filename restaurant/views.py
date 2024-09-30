from django.shortcuts import render
import random

# View for the main page
def main(request):
    return render(request, 'restaurant/main.html')


# View for the order page
def order(request):
    # Daily special from a list of Japanese dishes
    daily_special = random.choice(['Unagi Don', 'Tempura Udon', 'Sukiyaki', 'Tonkatsu'])
    context = {'daily_special': daily_special}
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        items = request.POST.getlist('menu_items')
        toppings = request.POST.getlist('toppings') 
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email')
        instructions = request.POST.get('instructions')

 
        total_price = 0
        for item in items:
            price_key = f'prices_{item}'  
            price = request.POST.get(price_key)
            if price:
                total_price += int(price)
        

        for topping in toppings:
            if topping == "Extra Fish":
                total_price += 5
            elif topping == "Wasabi":
                total_price += 2


        import time
        ready_time = time.strftime('%H:%M', time.localtime(time.time() + random.randint(30, 60) * 60))

        context = {
            'items': items,
            'toppings': toppings,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'instructions': instructions,
            'total_price': total_price,
            'ready_time': ready_time,
        }
        return render(request, 'restaurant/confirmation.html', context)
